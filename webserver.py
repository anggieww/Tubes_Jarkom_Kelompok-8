# import library yang akan digunakan
# pertama-tama kita membuat socket TCP pada server yang akan digunakan untuk menerima permintaan dari klien dan mengirimkan respon kembali ke klien
from socket import *
# os import merupakan library yang digunakan untuk mengakses file yang ada pada server
from os import path

# membangun TCP socket
# AF_INET untuk menentukan penggunaan alamat ip versi 4
# SOCK_STREAM untuk menentukan penggunaan TCP
#
serverSocket = socket(AF_INET, SOCK_STREAM)


# menghubungkan socket ke alamt ip dan juga port
# localhost untuk menentukan bahwa server akan berjalan pada komputer yang sama
# 8080 untuk menentukan port yang akan digunakan

serverSocket.bind(('localhost', 8080))


# serverSocket adalah socket yang akan digunakan untuk menerima koneksi dari klien
# listening socket yang akan digunakan untuk menerima permintaan koneksi dari klien
serverSocket.listen(1)

# looping ini adalah ketika server dijalankan maka akan selalu berjalan dan menerima permintaan dari klien dan
# mengirimkan respon kembali ke klien
while True:
    # output dibawah ini adalah menampilkan bahwa server sudah berjalan
    print("Server is running")
    # menerima koneksi dari klien serta menampilkan informasi klien
    # connectionSocket adalah socket yang akan digunakan untuk mengirim dan menerima data dari klien, addr adalah alamat klien
    # dan serversocket.accept adalah fungsi untuk menerima permintaan koneksi dari klien
    connectionSocket, addr = serverSocket.accept()
    # output dibawah ini adalah menampilkan informasi klien yang terhubung ke server
    print(f"Connection from {addr[0]}:{addr[1]}")

    try:
        # menerima request dari client
        # message adalah variabel yang digunakan untuk menampung request dari klien, recv(1024) adalah fungsi untuk menerima data dari klien
        # decode adalah fungsi untuk mengubah data yang diterima menjadi string
        message = connectionSocket.recv(1024).decode()
        # menerima file dari request
        # filename adalah variabel yang digunakan untuk menampung nama file yang akan diakses
        filename = message.split()[1]
        print(filename)
        # membaca file yang akan diakses dan [1:] adalah untuk menghilangkan karakter '/' pada nama file
        f = open(filename[1:])
        # outputdata adalah variabel yang digunakan untuk menampung isi dari file yang akan diakses
        outputdata = f.read()
        # menutup file yang akan diakses
        f.close()

        # mengirimkan respon terhadap klien
        # connectionSocket.send adalah fungsi untuk mengirimkan data ke klien dan
        # 'HTTP/1.0 200 OK\r\n\r\n'.encode() : http/1.0 adalah versi http yang digunakan, 200 adalah kode status yang menunjukkan bahwa permintaan berhasil
        # dan OK adalah pesan yang menunjukkan bahwa permintaan berhasil dan \r\n\r\n adalah fungsi untuk membuat baris baru, encode() adalah fungsi untuk mengubah string menjadi byte
        connectionSocket.send('HTTP/1.0 200 OK\r\n\r\n'.encode())
        # looping untuk mengirimkan data yang telah di encode
        for i in range(0, len(outputdata)):
            try:
                # mengirimkan setiap karakter yang di encode
                connectionSocket.send(outputdata[i].encode())
            # except merupakan kondisi apabila terjadi error seperti koneksi terputus, maka connectionSocket akan ditutup, connectionResetError adalah error yang terjadi apabila koneksi terputus
            except (ConnectionAbortedError, ConnectionResetError):
                break

        # connectionSocket.shutdown(SHUT_WR) adalah fungsi untuk menutup koneksi socket
        connectionSocket.shutdown(SHUT_WR)
        # connectionSocket.close() adalah fungsi untuk menutup koneksi socket
        connectionSocket.close()
    # kondisi apabila terjadi error
    except IOError:
        # menampilkan pesan not found kepada client
        print("404 Page Not Found")
        # mengirimkan respon terhadap klien
        connectionSocket.send('HTTP/1.0 404 Not Found\r\n\r\n'.encode())

        # Membuka file error.html jika terjadi kesalahan
        error_file = open('error.html', 'rb')
        error_content = error_file.read()
        error_file.close()

        # menutup koneksi socket
        connectionSocket.send(error_content)
        connectionSocket.close()

# menutup socket server
serverSocket.close()
