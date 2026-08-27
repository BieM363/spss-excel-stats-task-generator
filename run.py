"""
Launcher Script for Generator Tugas Random SPSS & Excel
Author: BieM363 (https://github.com/BieM363)
Usage: python run.py
"""

import sys
import os
import uvicorn
import webbrowser
import threading
import time

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    print("=" * 70)
    print(">> Memulai Generator Tugas Random SPSS & Excel (300 Bank Soal)")
    print("   Dibuat & Dikembangkan oleh: BieM363")
    print("   Server berjalan di: http://localhost:8000")
    print("=" * 70)
    
    # Auto open browser
    threading.Thread(target=open_browser, daemon=True).start()
    
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
