import os
import socket
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_wifi_ip():
    try:
        return "192.168.1.6"  # Your Wi-Fi IP address
    except:
        return "127.0.0.1"

def setup_hosts():
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    ip_address = get_wifi_ip()
    
    # Check if the mapping already exists
    with open(hosts_path, 'r') as f:
        content = f.read()
        if "lan.lounge" in content:
            print("lan.lounge mapping already exists in hosts file")
            return

    # Add the mapping
    with open(hosts_path, 'a') as f:
        f.write(f"\n{ip_address} lan.lounge\n")
    
    print(f"Added lan.lounge -> {ip_address} mapping to hosts file")
    print("You can now access the chat at: http://lan.lounge:3000")

if __name__ == "__main__":
    if not is_admin():
        print("Please run this script as Administrator")
        sys.exit(1)
    
    setup_hosts() 