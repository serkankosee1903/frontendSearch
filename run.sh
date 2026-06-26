#!/bin/bash
# ─────────────────────────────────────────────────────
# 🚀 ilanSearch Kurulum ve Başlatma Scripti
# ─────────────────────────────────────────────────────

set -e

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║   🚀 Senior Front-End İlan Bulucu - Kurulum     ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# Python sürümünü kontrol et
PYTHON=$(which python3 || which python)
if [ -z "$PYTHON" ]; then
  echo "❌ Python bulunamadı. Lütfen Python 3.9+ yükleyin."
  exit 1
fi

echo "✅ Python: $($PYTHON --version)"

# Virtual environment oluştur
if [ ! -d ".venv" ]; then
  echo ""
  echo "📦 Virtual environment oluşturuluyor..."
  $PYTHON -m venv .venv
fi

# Aktivasyon
source .venv/bin/activate
echo "✅ Virtual environment aktif"

# Bağımlılıkları yükle
echo ""
echo "📦 Bağımlılıklar yükleniyor..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "✅ Bağımlılıklar yüklendi"

# output klasörü
mkdir -p output

echo ""
echo "═══════════════════════════════════════════════════"
echo "🔍 Kariyer sayfaları taranıyor..."
echo "   (Bu işlem 2-5 dakika sürebilir)"
echo "═══════════════════════════════════════════════════"
echo ""

# Scraper'ı çalıştır
python scraper.py

# Telegram bildirimlerini gönder (Eğer yapılandırıldıysa)
python telegram_notifier.py

# Dashboard'u aç
if [ -f "output/report.html" ]; then
  cp output/report.html index.html
  echo ""
  echo "🌐 Dashboard açılıyor..."
  open output/report.html 2>/dev/null || xdg-open output/report.html 2>/dev/null || echo "Tarayıcıda açın: output/report.html"
fi

echo ""
echo "✅ Tamamlandı!"
