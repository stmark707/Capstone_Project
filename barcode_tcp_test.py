import socket

HOST = '192.168.1.24'
PORT = 9004

BARCODE_SCANNER = '192.168.1.10'
BARCODE_PORT = 9004

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as message_path:
        #message_path.bind((HOST, PORT))
        #message_path.listen()
        message_path.connect((BARCODE_SCANNER, BARCODE_PORT))
        message_path.sendall(b'LON')
        
        data = message_path.recv(1024)
        print(f'data received = {data!r}')
            
        
except KeyboardInterrupt:
    print('system cancel')