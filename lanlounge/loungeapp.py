import os
import random
import string
from flask import Flask, render_template, request, send_from_directory, session, redirect, url_for, flash
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
from zeroconf import ServiceInfo, Zeroconf
import socket
import sqlite3
from datetime import datetime, timedelta
import threading
import time
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DATABASE'] = 'chat.db'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'zip'}
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store connected users and their usernames
connected_users = {}

def init_db():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                filename TEXT NOT NULL,
                filepath TEXT NOT NULL,
                filetype TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

def get_local_ip():
    try:
        # Create a socket to determine the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def register_mdns():
    try:
        print("Starting mDNS registration...")
        zeroconf = Zeroconf()
        local_ip = get_local_ip()
        print(f"Local IP detected: {local_ip}")
        
        # Create a DNS-compliant service name (no spaces, lowercase)
        service_name = "lanlounge"
        service_type = "_http._tcp.local."
        service_name_full = f"{service_name}.{service_type}"
        
        # Register the service with proper DNS naming
        info = ServiceInfo(
            service_type,
            service_name_full,
            addresses=[socket.inet_aton(local_ip)],
            port=3000,
            properties={
                "path": "/",
                "name": "LAN Lounge Chat",  # Display name can have spaces
                "version": "1.0"
            },
            server=f"{service_name}.local."
        )
        
        print(f"Attempting to register mDNS service: {service_name_full}")
        zeroconf.register_service(info)
        print(f"\n=== LAN LOUNGE CHAT SERVER ===")
        print(f"Host machine can access at: http://localhost:3000")
        print(f"Other devices can access at: http://{service_name}.local:3000")
        print(f"Or use IP address: http://{local_ip}:3000")
        print("==============================\n")
        return zeroconf
    except Exception as e:
        print(f"Warning: mDNS registration failed with error: {str(e)}")
        print("The chat will still work at http://localhost:3000")
        return None

def generate_username():
    adjectives = ['Blue', 'Red', 'Green', 'Purple', 'Yellow', 'Orange', 'Pink', 'Black', 'White', 'Silver']
    animals = ['Tiger', 'Lion', 'Eagle', 'Wolf', 'Bear', 'Fox', 'Hawk', 'Dolphin', 'Shark', 'Panda']
    return f"{random.choice(adjectives)}{random.choice(animals)}"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return redirect(url_for('set_username'))

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('set_username'))
    return render_template('index.html', username=session['username'])

@app.route('/set-username', methods=['GET', 'POST'])
def set_username():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if username:
            session['username'] = username
            return redirect(url_for('chat'))
    return render_template('set_username.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@socketio.on('connect')
def handle_connect():
    if 'username' not in session:
        session['username'] = generate_username()
    username = session['username']
    connected_users[request.sid] = username
    emit('username_assigned', {'username': username})
    emit('user_joined', {'username': username}, broadcast=True)
    
    # Send message history
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.execute('SELECT username, message, timestamp FROM messages ORDER BY timestamp DESC LIMIT 50')
        messages = [{'username': row[0], 'message': row[1], 'timestamp': row[2]} for row in cursor.fetchall()]
        emit('message_history', {'messages': messages})

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in connected_users:
        username = connected_users[request.sid]
        del connected_users[request.sid]
        emit('user_left', {'username': username}, broadcast=True)

@socketio.on('chat_message')
def handle_message(data):
    username = session.get('username', connected_users.get(request.sid))
    message = data['message']
    
    # Save message to database
    with sqlite3.connect(app.config['DATABASE']) as conn:
        conn.execute('INSERT INTO messages (username, message) VALUES (?, ?)',
                    (username, message))
    
    emit('chat_message', {
        'username': username,
        'message': message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }, broadcast=True)

@socketio.on('file_upload')
def handle_file_upload(data):
    username = session.get('username', connected_users.get(request.sid))
    filename = secure_filename(data['filename'])
    
    if not allowed_file(filename):
        emit('error', {'message': 'File type not allowed'})
        return
        
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_type = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    try:
        # Decode base64 data and save the file
        file_data = base64.b64decode(data['file_data'])
        with open(file_path, 'wb') as f:
            f.write(file_data)
        
        # Save file info to database
        with sqlite3.connect(app.config['DATABASE']) as conn:
            conn.execute('INSERT INTO files (username, filename, filepath, filetype) VALUES (?, ?, ?, ?)',
                        (username, filename, file_path, file_type))
        
        # Broadcast file to all users
        file_url = f"/uploads/{filename}"
        
        # Check if it's an image file
        is_image = file_type in {'png', 'jpg', 'jpeg', 'gif'}
        
        emit('chat_message', {
            'username': username,
            'message': f"Shared a file: {filename}",
            'file_url': file_url,
            'file_type': file_type,
            'is_image': is_image,  # Add flag for image files
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }, broadcast=True)
    except Exception as e:
        print(f"Error uploading file: {e}")  # Add logging
        emit('error', {'message': 'Error uploading file'})
        if os.path.exists(file_path):
            os.remove(file_path)

def cleanup_old_data():
    """Clean up old files and messages"""
    while True:
        try:
            # Clean up files older than 7 days
            with sqlite3.connect(app.config['DATABASE']) as conn:
                cursor = conn.execute('''
                    SELECT filepath FROM files 
                    WHERE timestamp < datetime('now', '-7 days')
                ''')
                old_files = cursor.fetchall()
                
                for (filepath,) in old_files:
                    if os.path.exists(filepath):
                        os.remove(filepath)
                
                # Delete old file records
                conn.execute('DELETE FROM files WHERE timestamp < datetime("now", "-7 days")')
                
                # Delete old messages (keep last 1000 messages)
                conn.execute('''
                    DELETE FROM messages 
                    WHERE id NOT IN (
                        SELECT id FROM messages 
                        ORDER BY timestamp DESC 
                        LIMIT 1000
                    )
                ''')
                
                conn.commit()
        except Exception as e:
            print(f"Error during cleanup: {e}")
        
        time.sleep(3600)  # Run cleanup every hour

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Start cleanup thread
    cleanup_thread = threading.Thread(target=cleanup_old_data, daemon=True)
    cleanup_thread.start()
    
    # Get the actual local IP
    local_ip = get_local_ip()
    
    try:
        # Register mDNS service
        zeroconf = register_mdns()
        
        # Run on all network interfaces
        socketio.run(app, 
                    host='0.0.0.0',  # This makes it accessible from any network interface
                    port=3000, 
                    debug=True, 
                    allow_unsafe_werkzeug=True)
    except Exception as e:
        print(f"Error starting server: {str(e)}")
    finally:
        if zeroconf:
            zeroconf.unregister_all_services()
            zeroconf.close() 