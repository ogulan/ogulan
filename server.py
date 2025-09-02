#!/usr/bin/env python3
import http.server
import socketserver
import os

# Zmień katalog roboczy na folder ze stroną
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
        print(f"🚀 Serwer uruchomiony na http://localhost:{PORT}")
        print(f"📂 Serwuje pliki z: {os.getcwd()}")
        print("📱 Otwórz w przeglądarce: http://localhost:8000")
        print("\n⚠️  Aby zatrzymać serwer, naciśnij Ctrl+C")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Serwer zatrzymany")
