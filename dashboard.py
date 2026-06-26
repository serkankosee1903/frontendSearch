#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 İlan Dashboard Sunucusu
==========================
Scraper çıktısını gerçek zamanlı olarak gösteren web sunucusu.
"""

import json
import http.server
import socketserver
import webbrowser
import threading
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "output"


def start_server(port: int = 8765):
    """Basit HTTP sunucusu başlatır."""
    import os
    os.chdir(OUTPUT_DIR)

    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *args: None  # Sessiz log

    with socketserver.TCPServer(("", port), handler) as httpd:
        url = f"http://localhost:{port}/report.html"
        print(f"🌐 Dashboard açılıyor: {url}")
        webbrowser.open(url)
        print("Durdurmak için Ctrl+C'ye basın...")
        httpd.serve_forever()


if __name__ == "__main__":
    report_path = OUTPUT_DIR / "report.html"
    if not report_path.exists():
        print("❌ Henüz rapor oluşturulmamış. Önce scraper.py'yi çalıştırın:")
        print("   python scraper.py")
    else:
        start_server()
