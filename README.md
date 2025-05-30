# LAN Lounge

A lightweight local web application for real-time chat and file sharing over your local network.

## Features

- Real-time chat messaging
- Anonymous usernames (automatically assigned)
- File and image sharing (images appear inline in chat)
- Works entirely over LAN
- Modern, responsive UI
- No internet connection required

## Requirements

- Python 3.7 or higher
- pip (Python package manager)

## Quick Start

1. **Clone or download this repository.**
2. **Open a terminal in the project folder.**
3. **Create a virtual environment (recommended):**
   ```
   python -m venv .venv
   ```
4. **Activate the virtual environment:**
   - Windows:
     ```
     .venv\Scripts\activate
     ```
   - Mac/Linux:
     ```
     source .venv/bin/activate
     ```
5. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
6. **Run the app:**
   ```
   python loungeapp.py
   ```

## Accessing from Other Devices

1. **Find your computer's IP address:**
   - **Windows:** Run `ipconfig` in Command Prompt and look for the "IPv4 Address" under your active network adapter.
   - **Mac/Linux:** Run `ifconfig` or `ip addr` in Terminal and look for your local network IP (e.g., `192.168.x.x`).
2. **On other devices (phones, tablets, laptops) connected to the same Wi-Fi or LAN:**
   - Open a web browser and enter:
     ```
     http://<your-ip-address>:3000
     ```
     (Replace `<your-ip-address>` with the IP you found above.)

## Optional: Friendly Name (mDNS)

- If your network supports mDNS, you can use `http://lanlounge.local:3000`
- On Windows, you may need to install [Bonjour Print Services](https://support.apple.com/kb/DL999?locale=en_US)

## File Sharing

- Click the paperclip icon (📎) to select and share files (images, docs, etc.)
- Images will appear directly in the chat
- Files are stored in the `uploads` directory
- Shared files are accessible to all users in the chat

## Security Note

This application is designed for use on trusted local networks only.  
It does not implement any authentication or encryption.  
**Do not use on untrusted or public networks.**

## License

MIT License 
