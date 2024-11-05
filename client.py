# client.py
import socket
import os
import time

class FileTransferClient:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        # Inisialisasi UDP socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Set timeout untuk mencegah hanging
        self.client_socket.settimeout(10)
        # Buffer untuk menerima data
        self.buffer_size = 1024
        
    def request_file(self, filename, save_path):
        try:
            server_address = (self.host, self.port)
            
            # Kirim request file ke server
            print(f"Meminta file: {filename}")
            self.client_socket.sendto(filename.encode(), server_address)
            
            # Terima ukuran file
            data, _ = self.client_socket.recvfrom(self.buffer_size)
            
            # Cek apakah ada pesan error
            try:
                file_size = int(data.decode())
                print(f"Ukuran file: {file_size} bytes")
            except ValueError:
                print(f"Error: {data.decode()}")
                return
            
            # Buat file untuk menyimpan data
            with open(save_path, 'wb') as file:
                bytes_received = 0
                start_time = time.time()
                
                while bytes_received < file_size:
                    try:
                        # Terima chunk data
                        chunk, _ = self.client_socket.recvfrom(self.buffer_size)
                        if not chunk:
                            break
                            
                        # Tulis chunk ke file
                        file.write(chunk)
                        bytes_received += len(chunk)
                        
                        # Hitung dan tampilkan progress
                        progress = (bytes_received / file_size) * 100
                        print(f"Progress: {progress:.2f}%", end='\r')
                        
                    except socket.timeout:
                        print("\nError: Timeout saat menerima data")
                        return
                    
                end_time = time.time()
                
            # Tampilkan statistik transfer
            duration = end_time - start_time
            speed = file_size / (1024 * 1024 * duration) # MB/s
            print(f"\nFile {filename} berhasil diterima")
            print(f"Waktu transfer: {duration:.2f} detik")
            print(f"Kecepatan transfer: {speed:.2f} MB/s")
            print(f"File disimpan sebagai: {save_path}")
            
        except socket.timeout:
            print("Error: Koneksi timeout")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.client_socket.close()

def main():
    # Minta input dari user
    server_host = input("Masukkan host server (default: localhost): ").strip() or 'localhost'
    try:
        server_port = int(input("Masukkan port server (default: 9999): ").strip() or '9999')
    except ValueError:
        print("Port harus berupa angka. Menggunakan port default 9999")
        server_port = 9999
        
    client = FileTransferClient(server_host, server_port)
    
    while True:
        try:
            # Minta nama file yang akan diminta
            filename = input("\nMasukkan nama file yang ingin diminta (atau 'exit' untuk keluar): ").strip()
            if filename.lower() == 'exit':
                break
                
            if not filename:
                print("Nama file tidak boleh kosong")
                continue
                
            # Tentukan nama file untuk menyimpan
            save_path = input(f"Masukkan nama file untuk menyimpan (default: received_{filename}): ").strip() \
                       or f"received_{filename}"
                       
            # Request file
            client.request_file(filename, save_path)
            
        except KeyboardInterrupt:
            print("\nProgram dihentikan")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    main()