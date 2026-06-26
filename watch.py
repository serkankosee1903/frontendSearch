#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⏰ Otomatik İlan Takip Scripti
===============================
Düzenli aralıklarla kariyer sayfalarını tarar, 
yeni ilanları bildirir.

Kullanım:
  python watch.py              # Her 4 saatte bir tara
  python watch.py --interval 2 # Her 2 saatte bir tara
  python watch.py --once       # Sadece bir kez çalıştır
"""

import json
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime, timezone

# Scraper'dan import et
sys.path.insert(0, str(Path(__file__).parent))
from scraper import main as run_scraper, OUTPUT_DIR

KNOWN_IDS_FILE = OUTPUT_DIR / "known_ids.json"


def load_known_ids() -> set:
    """Daha önce görülen ilan ID'lerini yükler."""
    if KNOWN_IDS_FILE.exists():
        with open(KNOWN_IDS_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_known_ids(ids: set):
    """Görülen ilan ID'lerini kaydeder."""
    with open(KNOWN_IDS_FILE, "w") as f:
        json.dump(list(ids), f)


def notify_new_jobs(new_jobs: list[dict]):
    """Yeni ilanlar için macOS bildirimi gönderir."""
    if not new_jobs:
        return

    import subprocess
    for job in new_jobs[:5]:  # Max 5 bildirim
        try:
            title = f"🚀 Yeni İlan: {job['company']}"
            message = job['title']
            script = (
                f'display notification "{message}" '
                f'with title "{title}" '
                f'sound name "Glass"'
            )
            subprocess.run(
                ["osascript", "-e", script],
                capture_output=True, timeout=5
            )
        except Exception:
            pass

    if len(new_jobs) > 5:
        try:
            script = (
                f'display notification "Ve {len(new_jobs)-5} ilan daha..." '
                f'with title "🚀 Yeni İlanlar Bulundu!"'
            )
            subprocess.run(["osascript", "-e", script], capture_output=True, timeout=5)
        except Exception:
            pass


def run_cycle():
    """Tek bir tarama döngüsü çalıştırır."""
    print(f"\n{'='*50}")
    print(f"⏰ Tarama başladı: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print(f"{'='*50}")

    known_ids = load_known_ids()
    jobs = run_scraper()

    if not jobs:
        print("📭 Hiç ilan bulunamadı.")
        return

    # Yeni ilanları bul
    new_jobs = [j for j in jobs if j["id"] not in known_ids]

    if new_jobs:
        print(f"\n🎉 {len(new_jobs)} YENİ İLAN!")
        for job in new_jobs:
            print(f"  ✨ [{job['company']}] {job['title']}")
            print(f"     🔗 {job['url']}")
        notify_new_jobs(new_jobs)
    else:
        print(f"\n✅ {len(jobs)} ilan bulundu, yeni ilan yok.")

    # Bilinen ID'leri güncelle
    all_ids = known_ids | {j["id"] for j in jobs}
    save_known_ids(all_ids)

    # HTML raporu aç
    html_path = OUTPUT_DIR / "report.html"
    if html_path.exists():
        import subprocess
        subprocess.run(["open", str(html_path)], capture_output=True)


def main():
    parser = argparse.ArgumentParser(
        description="Senior Front-End İlan Takip Botu"
    )
    parser.add_argument(
        "--interval", type=int, default=4,
        help="Tarama aralığı (saat, default: 4)"
    )
    parser.add_argument(
        "--once", action="store_true",
        help="Sadece bir kez çalıştır"
    )
    args = parser.parse_args()

    if args.once:
        run_cycle()
        return

    interval_seconds = args.interval * 3600
    print(f"⏰ Her {args.interval} saatte bir otomatik tarama yapılacak.")
    print("   Durdurmak için Ctrl+C'ye basın.")

    while True:
        try:
            run_cycle()
            next_run = datetime.now()
            next_run = next_run.replace(
                hour=next_run.hour + args.interval if next_run.hour + args.interval < 24
                else next_run.hour + args.interval - 24
            )
            print(f"\n💤 Sonraki tarama: {args.interval} saat sonra...")
            time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\n👋 İlan takibi durduruldu.")
            break
        except Exception as e:
            print(f"❌ Hata: {e}")
            print("⏳ 30 saniye sonra tekrar deneniyor...")
            time.sleep(30)


if __name__ == "__main__":
    main()
