#!/usr/bin/env python3
"""
Servidor HTTP simple para probar el landing page
"""
import http.server
import socketserver
import os

PORT = 8005
DIRECTORY = "/vercel/sandbox"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Agregar headers CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Redirigir / al landing
        if self.path == '/':
            self.path = '/landing/index.html'
        super().do_GET()

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"✨ Servidor corriendo en http://localhost:{PORT}")
        print(f"📁 Sirviendo archivos desde: {DIRECTORY}")
        print(f"🌐 Landing page: http://localhost:{PORT}/landing/index.html")
        print(f"🎨 Frontend: http://localhost:{PORT}/frontend/index.html")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor detenido")
