from socket import *
from os import path

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', 8080))
serverSocket.listen(1)

while True:
    print("Server is running")
    connectionSocket, addr = serverSocket.accept()
    print(f"Connection from {addr[0]}:{addr[1]}")

    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1] if len(message.split()) > 1 else None

        if filename is None:
            print("Invalid request")
            connectionSocket.send('HTTP/1.0 400 Bad Request\r\n\r\n'.encode())
            connectionSocket.close()
            continue

        print(filename)

        if not path.exists(filename[1:]):
            raise IOError

        f = open(filename[1:])
        outputdata = f.read()
        f.close()

        connectionSocket.send('HTTP/1.0 200 OK\r\n\r\n'.encode())
        for i in range(0, len(outputdata)):
            try:
                connectionSocket.send(outputdata[i].encode())
            except (ConnectionAbortedError, ConnectionResetError):
                break

        # Menutup koneksi untuk pengiriman data
        connectionSocket.shutdown(SHUT_WR)
        connectionSocket.close()

    except IOError:
        print("404 Page Not Found")
        connectionSocket.send('HTTP/1.0 404 Not Found\r\n\r\n'.encode())

        # Membuka file error.html jika terjadi kesalahan
        error_file = open('error.html', 'rb')
        error_content = error_file.read()
        error_file.close()

        connectionSocket.send(error_content)
        connectionSocket.close()

serverSocket.close()
