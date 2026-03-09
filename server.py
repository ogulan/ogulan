#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys
import socket
import webbrowser
from threading import Timer

# Zmień katalog roboczy na folder ze stroną
project_dir = os.path.dirname(os.path.abspath(__file__))
public_dir = os.path.join(project_dir, 'public')

if os.path.exists(public_dir):
    os.chdir(public_dir)
else:
    print(f"Błąd: Nie znaleziono katalogu {public_dir}")

# Funkcja do znajdowania wolnego portu
def find_free_port(start_port=8000, max_attempts=10):
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
    return None

PORT = find_free_port()
if PORT is None:
    print("Nie znaleziono wolnego portu w zakresie 8000-8010.")
    sys.exit(1)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Dodaj nagłówki CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        # Wyłącz cache dla łatwiejszego developmentu
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

# Allow address reuse to prevent "Address already in use" errors
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

def open_browser():
    webbrowser.open(f'http://localhost:{PORT}')

if __name__ == "__main__":
    try:
        with ThreadedTCPServer(('', PORT), MyHTTPRequestHandler) as httpd:
            print(f"✅ Serwer uruchomiony pomyślnie!")
            print(f"📂 Katalog główny: {os.getcwd()}")
            print(f"🔗 Adres: http://localhost:{PORT}")
            print("\nAby zatrzymać serwer, naciśnij Ctrl+C")
            
            # Otwórz przeglądarkę automatycznie po 1 sekundzie
            Timer(1, open_browser).start()
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Serwer zatrzymany przez użytkownika.")
    except Exception as e:
        print(f"\n❌ Wystąpił błąd: {e}")
