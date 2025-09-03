#!/usr/bin/env python3
import http.server
import socketserver
import os

# Zmień katalog roboczy na folder ze stroną
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public'))

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Dodaj nagłówki CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(('', PORT), MyHTTPRequestHandler) as httpd:
        print(f"Serwer uruchomiony na http://localhost:{PORT}")
        print(f"Serwuje pliki z: {os.getcwd()}")
        print("Otworz w przegladarce: http://localhost:8000")
        print("\nAby zatrzymac serwer, nacisnij Ctrl+C")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nSerwer zatrzymany")
