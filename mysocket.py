#coding: utf-8

def stop_serv():
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 8005))
    sock.send('SHUTDOWN')
    sock.close()

if __name__ == '__main__':
    stop_serv()
    
