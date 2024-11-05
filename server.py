# server.py
import socket
import os
import time

class FileTransferServer:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        # Inisialisasi UDP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))
        # Buffer untuk menerima data
        self.buffer_size = 1024
        
    def start(self):
        print(f"Server berjalan di {self.host}:{self.port}")
        print("Menunggu koneksi dari client...")
        
        while True:
            try:
                # Terima request dari client
                data, client_address = self.server_socket.recvfrom(self.buffer_size)
                filename = data.decode()
                print(f"\nMenerima permintaan file '{filename}' dari {client_address}")
                
                # Cek keberadaan file
                if os.path.exists(filename):
                    # Buka file dalam mode binary
                    with open(filename, 'rb') as file:
                        # Baca ukuran file
                        file_size = os.path.getsize(filename)
                        print(f"File ditemukan. Ukuran: {file_size} bytes")
                        
                        # Kirim ukuran file ke client
                        self.server_socket.sendto(str(file_size).encode(), client_address)
                        
                        # Kirim isi file
                        bytes_sent = 0
                        while bytes_sent < file_size:
                            # Baca chunk data
                            chunk = file.read(self.buffer_size)
                            if not chunk:
                                break
                                
                            # Kirim chunk ke client
                            self.server_socket.sendto(chunk, client_address)
                            bytes_sent += len(chunk)
                            
                            # Tampilkan progress
                            progress = (bytes_sent / file_size) * 100
                            print(f"Progress pengiriman: {progress:.2f}%", end='\r')
                            
                            # Simulasi delay untuk demonstrasi
                            time.sleep(0.001)
                            
                        print(f"\nFile {filename} berhasil dikirim ke {client_address}")
                        
                else:
                    # Kirim pesan error jika file tidak ditemukan
                    print(f"File '{filename}' tidak ditemukan")
                    error_msg = "File tidak ditemukan"
                    self.server_socket.sendto(error_msg.encode(), client_address)
                    
            except Exception as e:
                print(f"Error: {e}")
                continue

if __name__ == "__main__":
    try:
        server = FileTransferServer()
        server.start()
    except KeyboardInterrupt:
        print("\nServer dihentikan")
    except Exception as e:
        print(f"Error: {e}")