#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import time
from pathlib import Path
import requests

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "output"
LATEST_FILE = OUTPUT_DIR / "latest.json"
SENT_JOBS_FILE = OUTPUT_DIR / "sent_jobs.json"
ENV_FILE = SCRIPT_DIR / ".env"

def load_env():
    """Simple .env parser"""
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200
    except Exception as e:
        print(f"Telegram error: {e}")
        return False

def main():
    load_env()
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("Telegram BOT_TOKEN or CHAT_ID not configured. Skipping notifications.")
        return

    if not LATEST_FILE.exists():
        print("latest.json not found. Skipping notifications.")
        return

    try:
        with open(LATEST_FILE, "r", encoding="utf-8") as f:
            latest_jobs = json.load(f)
    except Exception as e:
        print(f"Error reading latest jobs: {e}")
        return

    sent_jobs = set()
    if SENT_JOBS_FILE.exists():
        try:
            with open(SENT_JOBS_FILE, "r", encoding="utf-8") as f:
                sent_jobs = set(json.load(f))
        except Exception:
            pass

    new_jobs = []
    for job in latest_jobs:
        if job["id"] not in sent_jobs:
            new_jobs.append(job)

    if not new_jobs:
        print("No new jobs to send.")
        return
        
    print(f"Found {len(new_jobs)} new jobs to notify via Telegram.")
    
    sent_count = 0
    for job in new_jobs:
        msg = f"🚀 <b>YENİ İLAN BULDUM!</b>\n\n"
        msg += f"🏢 <b>Firma:</b> {job['company']}\n"
        msg += f"👨‍💻 <b>Pozisyon:</b> {job['title']}\n"
        msg += f"📍 <b>Konum:</b> {job['location']}\n"
        msg += f"🌐 <b>Kaynak:</b> {job['source']}\n\n"
        msg += f"<a href='{job['url']}'>🔗 İlana Git / Başvur</a>"
        
        if send_telegram_message(bot_token, chat_id, msg):
            sent_jobs.add(job["id"])
            sent_count += 1
            time.sleep(1) # Prevent hitting rate limits
            
    # Save the updated sent jobs back
    try:
        with open(SENT_JOBS_FILE, "w", encoding="utf-8") as f:
            json.dump(list(sent_jobs), f, ensure_ascii=False)
        print(f"Successfully sent {sent_count} messages and updated sent_jobs.json.")
    except Exception as e:
        print(f"Error saving sent_jobs.json: {e}")

if __name__ == "__main__":
    main()
