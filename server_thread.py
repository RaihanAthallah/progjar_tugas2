from socket import *
import socket
import threading
import logging
import datetime
import pytz

class ProcessTheClient(threading.Thread):
    def __init__(self,connection,address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        while True:
            
            data = self.connection.recv(1024).decode('utf-8')

            # Mengecek apakah pesan yang diterima dari client mengandung string 'WAKTU SEKARANG'
            if data.startswith('JAM') and data.endswith('\r\n'):
                # Kemudian atur timezone server ke Asia/Jakarta
                indonesia_timezone = pytz.timezone('Asia/Jakarta')
                # Dapatkan waktu server saat ini
                indonesia_server_time = datetime.datetime.now(tz=indonesia_timezone)
                # Ubah format waktu server menjadi HH:MM:SS
                indonesia_time_str = indonesia_server_time.strftime('%H:%M:%S')
                # kirim waktu server ke client
                response = f'JAM {indonesia_time_str}\r\n'
                self.connection.send(response.encode('utf-8'))
            else:
                break
        self.connection.close()

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('localhost',45000))
        self.my_socket.listen(5)
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"connection from {self.client_address}")

            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)


def main():
    svr = Server()
    svr.start()

if __name__=="__main__":
    main()