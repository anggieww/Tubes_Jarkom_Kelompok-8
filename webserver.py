from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 8888))
serverSocket.listen(1)
while True:
    print("Server is running")
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1].decode('utf-8').strip("/")
        print(filename)
        f = open(filename)
        outputdata = f.read()
        f.close()
        connectionSocket.send('HTTP/1.0 200 OK\r\n\r\n'.encode())
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.close()
    except IOError:
        print("404 Page Not Found")
        connectionSocket.send('HTTP/1.0 404 Not Found\r\n\r\n'.encode())
        connectionSocket.send(
            b'<html><head></head><body><h1>404 Not Found</h1></body></html>')
        connectionSocket.close()
serverSocket.close()
