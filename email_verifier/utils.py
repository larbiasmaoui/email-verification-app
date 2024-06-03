import socket

def check_internet_connection():
    try:    
        # connect Google's DNS server
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False
