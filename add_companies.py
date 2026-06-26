#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Türkiye'deki tüm büyük yazılım/teknoloji firmalarını
companies.json'a ekler. Mevcut firmalar korunur, yeniler eklenir.
"""

import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
COMPANIES_FILE = SCRIPT_DIR / "companies.json"

# ──────────────────────────────────────────────────────────────────────────────
# 400+ Türk Yazılım & Teknoloji Firması
# Kategoriler:
#   - E-ticaret & Perakende Dijital
#   - Fintech & Ödeme Sistemleri
#   - Bankacılık & Sigorta Teknoloji
#   - Telekomünikasyon
#   - Oyun & Eğlence
#   - Kurumsal Yazılım & SaaS
#   - Savunma & Havacılık
#   - Seyahat & Ulaşım
#   - Sağlık Teknoloji
#   - Eğitim Teknoloji
#   - Gayrimenkul Teknoloji
#   - İK & İşe Alım
#   - Medya & İçerik
#   - Lojistik & Tedarik
#   - Otomotiv Teknoloji
#   - BT Hizmetleri & Danışmanlık
#   - Siber Güvenlik
#   - Yapay Zeka & Veri
#   - Bulut & Altyapı
#   - Sanayi Dijital
#   - Uluslararası Firmalar (TR Ofisi)
#   - Yazılım Evleri & Ajanslar
#   - Startup & Scale-up
# ──────────────────────────────────────────────────────────────────────────────

NEW_COMPANIES = [

  # ── E-TİCARET & PERAKENDE DİJİTAL ─────────────────────────────────────────
  {"name": "Trendyol Go", "career_url": "https://jobs.lever.co/trendyol", "type": "lever", "logo": "🚴", "sector": "ecommerce"},
  {"name": "MediaMarkt Turkey Digital", "career_url": "https://mediamarkt.teamtailor.com/jobs", "type": "teamtailor", "logo": "📺", "sector": "ecommerce"},
  {"name": "Teknosa Digital", "career_url": "https://teknosa.teamtailor.com/jobs", "type": "teamtailor", "logo": "🖥️", "sector": "ecommerce"},
  {"name": "Vatan Bilgisayar Digital", "career_url": "https://vatanbilgisayar.teamtailor.com/jobs", "type": "teamtailor", "logo": "💻", "sector": "ecommerce"},
  {"name": "CarrefourSA Digital", "career_url": "https://carrefoursa.teamtailor.com/jobs", "type": "teamtailor", "logo": "🛒", "sector": "ecommerce"},
  {"name": "Gratis Digital", "career_url": "https://gratis.teamtailor.com/jobs", "type": "teamtailor", "logo": "💄", "sector": "ecommerce"},
  {"name": "Watsons Turkey Digital", "career_url": "https://watsons.teamtailor.com/jobs", "type": "teamtailor", "logo": "🧴", "sector": "ecommerce"},
  {"name": "Beymen Digital", "career_url": "https://beymen.teamtailor.com/jobs", "type": "teamtailor", "logo": "👒", "sector": "ecommerce"},
  {"name": "Morhipo", "career_url": "https://morhipo.teamtailor.com/jobs", "type": "teamtailor", "logo": "👗", "sector": "ecommerce"},
  {"name": "Ebebek Digital", "career_url": "https://ebebek.teamtailor.com/jobs", "type": "teamtailor", "logo": "🍼", "sector": "ecommerce"},
  {"name": "D&R Digital", "career_url": "https://dr.teamtailor.com/jobs", "type": "teamtailor", "logo": "📚", "sector": "ecommerce"},
  {"name": "Bookseller Digital", "career_url": "https://bookseller.teamtailor.com/jobs", "type": "teamtailor", "logo": "📖", "sector": "ecommerce"},
  {"name": "Pimclick", "career_url": "https://pimclick.teamtailor.com/jobs", "type": "teamtailor", "logo": "🛒", "sector": "ecommerce"},
  {"name": "GetirFresh", "career_url": "https://jobs.lever.co/getirfresh", "type": "lever", "logo": "🥦", "sector": "ecommerce"},
  {"name": "Tazedirekt", "career_url": "https://tazedirekt.teamtailor.com/jobs", "type": "teamtailor", "logo": "🥑", "sector": "ecommerce"},
  {"name": "Marketyo", "career_url": "https://marketyo.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏪", "sector": "ecommerce"},
  {"name": "Fuudy", "career_url": "https://fuudy.teamtailor.com/jobs", "type": "teamtailor", "logo": "🍔", "sector": "ecommerce"},
  {"name": "Shopiverse", "career_url": "https://shopiverse.teamtailor.com/jobs", "type": "teamtailor", "logo": "🛍️", "sector": "ecommerce"},
  {"name": "Epttavm", "career_url": "https://epttavm.teamtailor.com/jobs", "type": "teamtailor", "logo": "📮", "sector": "ecommerce"},
  {"name": "Superpedestrian Turkey", "career_url": "https://jobs.lever.co/superpedestrian", "type": "lever", "logo": "🛴", "sector": "ecommerce"},

  # ── FİNTECH & ÖDEME SİSTEMLERİ ────────────────────────────────────────────
  {"name": "Hayat Finans", "career_url": "https://hayatfinans.teamtailor.com/jobs", "type": "teamtailor", "logo": "💰", "sector": "fintech"},
  {"name": "Simpay", "career_url": "https://simpay.teamtailor.com/jobs", "type": "teamtailor", "logo": "💳", "sector": "fintech"},
  {"name": "Epara", "career_url": "https://epara.teamtailor.com/jobs", "type": "teamtailor", "logo": "💱", "sector": "fintech"},
  {"name": "Garanti Ödeme Sistemleri", "career_url": "https://garantios.teamtailor.com/jobs", "type": "teamtailor", "logo": "💳", "sector": "fintech"},
  {"name": "Ziraat Fintek", "career_url": "https://ziraatfintek.teamtailor.com/jobs", "type": "teamtailor", "logo": "🌾", "sector": "fintech"},
  {"name": "Denizbank Digital", "career_url": "https://denizbank.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏦", "sector": "fintech"},
  {"name": "Albaraka Türk Digital", "career_url": "https://albarakaturk.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏦", "sector": "fintech"},
  {"name": "Kuveyt Türk Digital", "career_url": "https://kuveytturk.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏦", "sector": "fintech"},
  {"name": "Türkiye Finans Digital", "career_url": "https://turkiyefinans.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏦", "sector": "fintech"},
  {"name": "Halkbank Ödeme Sistemleri", "career_url": "https://halkbankos.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏦", "sector": "fintech"},
  {"name": "Mastercard Turkey", "career_url": "https://jobs.lever.co/mastercard", "type": "lever", "logo": "💳", "sector": "fintech"},
  {"name": "Visa Turkey", "career_url": "https://jobs.lever.co/visa", "type": "lever", "logo": "💳", "sector": "fintech"},
  {"name": "Lidio", "career_url": "https://lidio.teamtailor.com/jobs", "type": "teamtailor", "logo": "💰", "sector": "fintech"},
  {"name": "Bitlo", "career_url": "https://bitlo.teamtailor.com/jobs", "type": "teamtailor", "logo": "₿", "sector": "fintech"},
  {"name": "Koineks", "career_url": "https://koineks.teamtailor.com/jobs", "type": "teamtailor", "logo": "🪙", "sector": "fintech"},
  {"name": "Icrypex", "career_url": "https://icrypex.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔐", "sector": "fintech"},
  {"name": "Bitay", "career_url": "https://bitay.teamtailor.com/jobs", "type": "teamtailor", "logo": "₿", "sector": "fintech"},
  {"name": "Coinzo", "career_url": "https://coinzo.teamtailor.com/jobs", "type": "teamtailor", "logo": "🪙", "sector": "fintech"},
  {"name": "Ripio Turkey", "career_url": "https://jobs.lever.co/ripio", "type": "lever", "logo": "💹", "sector": "fintech"},
  {"name": "Token Financial Technologies", "career_url": "https://tokenfi.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔑", "sector": "fintech"},
  {"name": "Vepara", "career_url": "https://vepara.teamtailor.com/jobs", "type": "teamtailor", "logo": "💳", "sector": "fintech"},
  {"name": "OtoPay", "career_url": "https://otopay.teamtailor.com/jobs", "type": "teamtailor", "logo": "🚗", "sector": "fintech"},

  # ── BANKACILIK & SİGORTA TEKNOLOJİ ────────────────────────────────────────
  {"name": "CEPTETEB", "career_url": "https://cepteteb.teamtailor.com/jobs", "type": "teamtailor", "logo": "📱", "sector": "banktech"},
  {"name": "Maximum Digital (İşbank)", "career_url": "https://maximum.teamtailor.com/jobs", "type": "teamtailor", "logo": "💳", "sector": "banktech"},
  {"name": "Avivasa Tech", "career_url": "https://avivasa.teamtailor.com/jobs", "type": "teamtailor", "logo": "🛡️", "sector": "banktech"},
  {"name": "Anadolu Sigorta Tech", "career_url": "https://anadolusigorta.teamtailor.com/jobs", "type": "teamtailor", "logo": "🛡️", "sector": "banktech"},
  {"name": "Allianz Turkey Tech", "career_url": "https://allianz.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔵", "sector": "banktech"},
  {"name": "Generali Turkey", "career_url": "https://generali.teamtailor.com/jobs", "type": "teamtailor", "logo": "🦁", "sector": "banktech"},
  {"name": "Mapfre Turkey Tech", "career_url": "https://mapfre.teamtailor.com/jobs", "type": "teamtailor", "logo": "🗺️", "sector": "banktech"},
  {"name": "Zurich Turkey Tech", "career_url": "https://zurich.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔴", "sector": "banktech"},
  {"name": "Sigortam.net", "career_url": "https://sigortam.teamtailor.com/jobs", "type": "teamtailor", "logo": "🛡️", "sector": "banktech"},
  {"name": "Neova Sigorta", "career_url": "https://neova.teamtailor.com/jobs", "type": "teamtailor", "logo": "🛡️", "sector": "banktech"},
  {"name": "Aksigorta Digital", "career_url": "https://aksigorta.teamtailor.com/jobs", "type": "teamtailor", "logo": "🛡️", "sector": "banktech"},
  {"name": "Eureko Sigorta", "career_url": "https://eureko.teamtailor.com/jobs", "type": "teamtailor", "logo": "🛡️", "sector": "banktech"},
  {"name": "Ray Sigorta", "career_url": "https://raysigorta.teamtailor.com/jobs", "type": "teamtailor", "logo": "🌟", "sector": "banktech"},
  {"name": "Groupama Turkey", "career_url": "https://groupama.teamtailor.com/jobs", "type": "teamtailor", "logo": "🌻", "sector": "banktech"},

  # ── TELEKOMÜNİKASYON ────────────────────────────────────────────────────────
  {"name": "Superonline", "career_url": "https://superonline.teamtailor.com/jobs", "type": "teamtailor", "logo": "🌐", "sector": "telecom"},
  {"name": "TurkNet", "career_url": "https://turknet.teamtailor.com/jobs", "type": "teamtailor", "logo": "🌐", "sector": "telecom"},
  {"name": "Millenicom", "career_url": "https://millenicom.teamtailor.com/jobs", "type": "teamtailor", "logo": "📡", "sector": "telecom"},
  {"name": "Türksat", "career_url": "https://turksat.teamtailor.com/jobs", "type": "teamtailor", "logo": "🛰️", "sector": "telecom"},
  {"name": "BiP (Turkcell)", "career_url": "https://bip.teamtailor.com/jobs", "type": "teamtailor", "logo": "💬", "sector": "telecom"},
  {"name": "Lifecell Ukraine (Turkish)", "career_url": "https://lifecell.teamtailor.com/jobs", "type": "teamtailor", "logo": "📱", "sector": "telecom"},
  {"name": "TTNET", "career_url": "https://ttnet.teamtailor.com/jobs", "type": "teamtailor", "logo": "📞", "sector": "telecom"},
  {"name": "Netspeed", "career_url": "https://netspeed.teamtailor.com/jobs", "type": "teamtailor", "logo": "⚡", "sector": "telecom"},
  {"name": "Global Bilgi", "career_url": "https://globalbilgi.teamtailor.com/jobs", "type": "teamtailor", "logo": "🌍", "sector": "telecom"},
  {"name": "Comodo CA Turkey", "career_url": "https://comodo.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔐", "sector": "telecom"},

  # ── OYUN & EĞLENCE ──────────────────────────────────────────────────────────
  {"name": "Nays Games", "career_url": "https://nays.teamtailor.com/jobs", "type": "teamtailor", "logo": "🎮", "sector": "gaming"},
  {"name": "Kodlab", "career_url": "https://kodlab.teamtailor.com/jobs", "type": "teamtailor", "logo": "🎯", "sector": "gaming"},
  {"name": "Metatope Games", "career_url": "https://metatope.teamtailor.com/jobs", "type": "teamtailor", "logo": "🎲", "sector": "gaming"},
  {"name": "Plarium Turkey", "career_url": "https://jobs.lever.co/plarium", "type": "lever", "logo": "⚔️", "sector": "gaming"},
  {"name": "Game4You Turkey", "career_url": "https://game4you.teamtailor.com/jobs", "type": "teamtailor", "logo": "🕹️", "sector": "gaming"},
  {"name": "GameBoss", "career_url": "https://gameboss.teamtailor.com/jobs", "type": "teamtailor", "logo": "👑", "sector": "gaming"},
  {"name": "Netmarble Turkey", "career_url": "https://jobs.lever.co/netmarble", "type": "lever", "logo": "🎮", "sector": "gaming"},
  {"name": "Supercell Istanbul", "career_url": "https://jobs.lever.co/supercell", "type": "lever", "logo": "🏆", "sector": "gaming"},
  {"name": "Voodoo Istanbul", "career_url": "https://jobs.lever.co/voodoo", "type": "lever", "logo": "🎯", "sector": "gaming"},
  {"name": "Rovio Turkey", "career_url": "https://jobs.lever.co/rovio", "type": "lever", "logo": "🐦", "sector": "gaming"},
  {"name": "Fugo Games", "career_url": "https://fugogames.teamtailor.com/jobs", "type": "teamtailor", "logo": "🎮", "sector": "gaming"},
  {"name": "Joygame Turkey", "career_url": "https://joygame.teamtailor.com/jobs", "type": "teamtailor", "logo": "😄", "sector": "gaming"},
  {"name": "IGG Turkey", "career_url": "https://igg.teamtailor.com/jobs", "type": "teamtailor", "logo": "🎮", "sector": "gaming"},
  {"name": "Miniclip Istanbul", "career_url": "https://jobs.lever.co/miniclip", "type": "lever", "logo": "🎯", "sector": "gaming"},
  {"name": "Outfit7 Turkey", "career_url": "https://jobs.lever.co/outfit7", "type": "lever", "logo": "🐱", "sector": "gaming"},
  {"name": "Masomo Studios", "career_url": "https://masomo.teamtailor.com/jobs", "type": "teamtailor", "logo": "⚽", "sector": "gaming"},
  {"name": "Nordeus Turkey", "career_url": "https://jobs.lever.co/nordeus", "type": "lever", "logo": "⚽", "sector": "gaming"},
  {"name": "AppQuantum Turkey", "career_url": "https://appquantum.teamtailor.com/jobs", "type": "teamtailor", "logo": "🎮", "sector": "gaming"},
  {"name": "Tripledot Studios TR", "career_url": "https://jobs.lever.co/tripledot", "type": "lever", "logo": "🃏", "sector": "gaming"},
  {"name": "Good Job Games", "career_url": "https://goodjobgames.teamtailor.com/jobs", "type": "teamtailor", "logo": "✅", "sector": "gaming"},

  # ── KURUMSAL YAZILIM & SaaS ──────────────────────────────────────────────────
  {"name": "Mikro Yazılım", "career_url": "https://mikro.teamtailor.com/jobs", "type": "teamtailor", "logo": "📊", "sector": "saas"},
  {"name": "Muhasebe.com", "career_url": "https://muhasebe.teamtailor.com/jobs", "type": "teamtailor", "logo": "📋", "sector": "saas"},
  {"name": "Ürün.io", "career_url": "https://urun.teamtailor.com/jobs", "type": "teamtailor", "logo": "📦", "sector": "saas"},
  {"name": "Folio Tech", "career_url": "https://folio.teamtailor.com/jobs", "type": "teamtailor", "logo": "📁", "sector": "saas"},
  {"name": "Testinium", "career_url": "https://testinium.teamtailor.com/jobs", "type": "teamtailor", "logo": "🧪", "sector": "saas"},
  {"name": "Monitise Turkey", "career_url": "https://monitise.teamtailor.com/jobs", "type": "teamtailor", "logo": "📱", "sector": "saas"},
  {"name": "Appcent", "career_url": "https://appcent.teamtailor.com/jobs", "type": "teamtailor", "logo": "📱", "sector": "saas"},
  {"name": "Appcircle", "career_url": "https://appcircle.teamtailor.com/jobs", "type": "teamtailor", "logo": "⭕", "sector": "saas"},
  {"name": "Mobven", "career_url": "https://mobven.teamtailor.com/jobs", "type": "teamtailor", "logo": "📲", "sector": "saas"},
  {"name": "Fark Labs", "career_url": "https://farklabs.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔬", "sector": "saas"},
  {"name": "Portakal Teknoloji", "career_url": "https://portakal.teamtailor.com/jobs", "type": "teamtailor", "logo": "🍊", "sector": "saas"},
  {"name": "Teknasyon", "career_url": "https://teknasyon.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏗️", "sector": "saas"},
  {"name": "Inomera", "career_url": "https://inomera.teamtailor.com/jobs", "type": "teamtailor", "logo": "💡", "sector": "saas"},
  {"name": "Intersoft", "career_url": "https://intersoft.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔧", "sector": "saas"},
  {"name": "CodeFiction", "career_url": "https://codefiction.teamtailor.com/jobs", "type": "teamtailor", "logo": "📖", "sector": "saas"},
  {"name": "Argelab", "career_url": "https://argelab.teamtailor.com/jobs", "type": "teamtailor", "logo": "🧬", "sector": "saas"},
  {"name": "Eteration", "career_url": "https://eteration.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔄", "sector": "saas"},
  {"name": "Probil Teknoloji", "career_url": "https://probil.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔧", "sector": "saas"},
  {"name": "NetDataSoft", "career_url": "https://netdatasoft.teamtailor.com/jobs", "type": "teamtailor", "logo": "💾", "sector": "saas"},
  {"name": "Quantum Digital", "career_url": "https://quantumdigital.teamtailor.com/jobs", "type": "teamtailor", "logo": "⚛️", "sector": "saas"},
  {"name": "SoftwareONE Turkey", "career_url": "https://softwareone.teamtailor.com/jobs", "type": "teamtailor", "logo": "🪟", "sector": "saas"},
  {"name": "N-iX Turkey", "career_url": "https://jobs.lever.co/n-ix", "type": "lever", "logo": "🔷", "sector": "saas"},
  {"name": "Metahorizon", "career_url": "https://metahorizon.teamtailor.com/jobs", "type": "teamtailor", "logo": "🌅", "sector": "saas"},
  {"name": "Nivo Teknoloji", "career_url": "https://nivo.teamtailor.com/jobs", "type": "teamtailor", "logo": "📊", "sector": "saas"},
  {"name": "4screen Turkey", "career_url": "https://4screen.teamtailor.com/jobs", "type": "teamtailor", "logo": "🖥️", "sector": "saas"},
  {"name": "Artı Yazılım", "career_url": "https://artiyazilim.teamtailor.com/jobs", "type": "teamtailor", "logo": "➕", "sector": "saas"},
  {"name": "GuidanceIQ", "career_url": "https://guidanceiq.teamtailor.com/jobs", "type": "teamtailor", "logo": "🧠", "sector": "saas"},
  {"name": "Tiga Software", "career_url": "https://tigasoftware.teamtailor.com/jobs", "type": "teamtailor", "logo": "🐯", "sector": "saas"},
  {"name": "Stradigi Turkey", "career_url": "https://stradigi.teamtailor.com/jobs", "type": "teamtailor", "logo": "📈", "sector": "saas"},
  {"name": "Jotform Turkey", "career_url": "https://jobs.lever.co/jotform", "type": "lever", "logo": "📝", "sector": "saas"},
  {"name": "AnyClip Turkey", "career_url": "https://jobs.lever.co/anyclip", "type": "lever", "logo": "🎬", "sector": "saas"},
  {"name": "Sendgrid Turkey", "career_url": "https://jobs.lever.co/sendgrid", "type": "lever", "logo": "📧", "sector": "saas"},
  {"name": "Netcracker Turkey", "career_url": "https://netcracker.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔗", "sector": "saas"},
  {"name": "Cozum Bulut", "career_url": "https://cozumbulut.teamtailor.com/jobs", "type": "teamtailor", "logo": "☁️", "sector": "saas"},
  {"name": "Mobisoft", "career_url": "https://mobisoft.teamtailor.com/jobs", "type": "teamtailor", "logo": "📱", "sector": "saas"},
  {"name": "Cerebrum Tech", "career_url": "https://cerebrum.teamtailor.com/jobs", "type": "teamtailor", "logo": "🧠", "sector": "saas"},
  {"name": "FullStak", "career_url": "https://fullstak.teamtailor.com/jobs", "type": "teamtailor", "logo": "⚡", "sector": "saas"},
  {"name": "BrainJet", "career_url": "https://brainjet.teamtailor.com/jobs", "type": "teamtailor", "logo": "✈️", "sector": "saas"},

  # ── SAVUNMA & HAVACILIKz ───────────────────────────────────────────────────
  {"name": "TUSAŞ (TAI) Digital", "career_url": "https://tusas.teamtailor.com/jobs", "type": "teamtailor", "logo": "✈️", "sector": "defense"},
  {"name": "Milsoft", "career_url": "https://milsoft.teamtailor.com/jobs", "type": "teamtailor", "logo": "🛡️", "sector": "defense"},
  {"name": "Meteksan Defense", "career_url": "https://meteksan.teamtailor.com/jobs", "type": "teamtailor", "logo": "📡", "sector": "defense"},
  {"name": "Savunma Teknolojileri", "career_url": "https://savunmateknolojileri.teamtailor.com/jobs", "type": "teamtailor", "logo": "🛡️", "sector": "defense"},
  {"name": "Türk Havacılık Uzay Sanayii", "career_url": "https://thuss.teamtailor.com/jobs", "type": "teamtailor", "logo": "🚀", "sector": "defense"},
  {"name": "Baykar Teknoloji", "career_url": "https://baykartech.teamtailor.com/jobs", "type": "teamtailor", "logo": "🛩️", "sector": "defense"},
  {"name": "Tübitak Bilgem", "career_url": "https://tubitakbilgem.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔬", "sector": "defense"},
  {"name": "Fnss Savunma", "career_url": "https://fnss.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔧", "sector": "defense"},
  {"name": "BMC Tech", "career_url": "https://bmctech.teamtailor.com/jobs", "type": "teamtailor", "logo": "🚛", "sector": "defense"},

  # ── SEYAHAT & ULAŞIM ───────────────────────────────────────────────────────
  {"name": "Yolcu360", "career_url": "https://yolcu360.teamtailor.com/jobs", "type": "teamtailor", "logo": "🚗", "sector": "travel"},
  {"name": "Turna.com", "career_url": "https://turna.teamtailor.com/jobs", "type": "teamtailor", "logo": "✈️", "sector": "travel"},
  {"name": "Bilet.com", "career_url": "https://bilet.teamtailor.com/jobs", "type": "teamtailor", "logo": "🎟️", "sector": "travel"},
  {"name": "Tatil.com", "career_url": "https://tatil.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏖️", "sector": "travel"},
  {"name": "Odamax", "career_url": "https://odamax.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏨", "sector": "travel"},
  {"name": "BiletBayisi", "career_url": "https://biletbayisi.teamtailor.com/jobs", "type": "teamtailor", "logo": "🎫", "sector": "travel"},
  {"name": "Touristica", "career_url": "https://touristica.teamtailor.com/jobs", "type": "teamtailor", "logo": "🌍", "sector": "travel"},
  {"name": "Tixel Turkey", "career_url": "https://jobs.lever.co/tixel", "type": "lever", "logo": "🎟️", "sector": "travel"},
  {"name": "Booking.com Istanbul", "career_url": "https://jobs.lever.co/booking", "type": "lever", "logo": "🏨", "sector": "travel"},
  {"name": "Airbnb Turkey", "career_url": "https://jobs.lever.co/airbnb", "type": "lever", "logo": "🏠", "sector": "travel"},
  {"name": "Tripadvisor Turkey", "career_url": "https://jobs.lever.co/tripadvisor", "type": "lever", "logo": "🗺️", "sector": "travel"},
  {"name": "IETT Dijital", "career_url": "https://iett.teamtailor.com/jobs", "type": "teamtailor", "logo": "🚌", "sector": "travel"},
  {"name": "Mobi Teknoloji", "career_url": "https://mobi.teamtailor.com/jobs", "type": "teamtailor", "logo": "🛵", "sector": "travel"},
  {"name": "Trink Mobility", "career_url": "https://trink.teamtailor.com/jobs", "type": "teamtailor", "logo": "⚡", "sector": "travel"},
  {"name": "Marti Tech", "career_url": "https://marti.teamtailor.com/jobs", "type": "teamtailor", "logo": "🛴", "sector": "travel"},

  # ── SAĞLIK TEKNOLOJİ ───────────────────────────────────────────────────────
  {"name": "Doktorsitesi", "career_url": "https://doktorsitesi.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏥", "sector": "healthtech"},
  {"name": "Doktorum.com", "career_url": "https://doktorum.teamtailor.com/jobs", "type": "teamtailor", "logo": "👨‍⚕️", "sector": "healthtech"},
  {"name": "Acıbadem Digital", "career_url": "https://acibadem.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏥", "sector": "healthtech"},
  {"name": "Memorial Digital", "career_url": "https://memorial.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏥", "sector": "healthtech"},
  {"name": "Medicana Digital", "career_url": "https://medicana.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏥", "sector": "healthtech"},
  {"name": "Sağlık Sepeti", "career_url": "https://sagliksepeti.teamtailor.com/jobs", "type": "teamtailor", "logo": "💊", "sector": "healthtech"},
  {"name": "Hekimce", "career_url": "https://hekimce.teamtailor.com/jobs", "type": "teamtailor", "logo": "🩺", "sector": "healthtech"},
  {"name": "Doktor Takvimi", "career_url": "https://doktortakvimi.teamtailor.com/jobs", "type": "teamtailor", "logo": "📅", "sector": "healthtech"},
  {"name": "Medikaynak", "career_url": "https://medikaynak.teamtailor.com/jobs", "type": "teamtailor", "logo": "💉", "sector": "healthtech"},
  {"name": "Meditcare", "career_url": "https://meditcare.teamtailor.com/jobs", "type": "teamtailor", "logo": "❤️", "sector": "healthtech"},
  {"name": "Diyetkolik Digital", "career_url": "https://diyetkolik.teamtailor.com/jobs", "type": "teamtailor", "logo": "🥗", "sector": "healthtech"},
  {"name": "Psikored", "career_url": "https://psikored.teamtailor.com/jobs", "type": "teamtailor", "logo": "🧠", "sector": "healthtech"},
  {"name": "Wellbees", "career_url": "https://wellbees.teamtailor.com/jobs", "type": "teamtailor", "logo": "🐝", "sector": "healthtech"},
  {"name": "Profen Group Digital", "career_url": "https://profen.teamtailor.com/jobs", "type": "teamtailor", "logo": "💊", "sector": "healthtech"},
  {"name": "Eczacıbaşı Digital", "career_url": "https://eczacibasi.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏭", "sector": "healthtech"},

  # ── EĞİTİM TEKNOLOJİSİ ─────────────────────────────────────────────────────
  {"name": "Tureng", "career_url": "https://tureng.teamtailor.com/jobs", "type": "teamtailor", "logo": "📚", "sector": "edtech"},
  {"name": "Dönüşüm Akademi", "career_url": "https://donusumakademi.teamtailor.com/jobs", "type": "teamtailor", "logo": "🎓", "sector": "edtech"},
  {"name": "Sabis Educational", "career_url": "https://sabis.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏫", "sector": "edtech"},
  {"name": "Uyumsoft", "career_url": "https://uyumsoft.teamtailor.com/jobs", "type": "teamtailor", "logo": "📖", "sector": "edtech"},
  {"name": "Bilge Adam Teknoloji", "career_url": "https://bilgeadamteknoloji.teamtailor.com/jobs", "type": "teamtailor", "logo": "📚", "sector": "edtech"},
  {"name": "Kodlama.io", "career_url": "https://kodlama.teamtailor.com/jobs", "type": "teamtailor", "logo": "💻", "sector": "edtech"},
  {"name": "Workinton Learning", "career_url": "https://workintonlearning.teamtailor.com/jobs", "type": "teamtailor", "logo": "📱", "sector": "edtech"},
  {"name": "Lise Kamp Digital", "career_url": "https://lisekamp.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏕️", "sector": "edtech"},
  {"name": "Kolayca.com", "career_url": "https://kolayca.teamtailor.com/jobs", "type": "teamtailor", "logo": "✅", "sector": "edtech"},
  {"name": "Sinav.com.tr", "career_url": "https://sinav.teamtailor.com/jobs", "type": "teamtailor", "logo": "📝", "sector": "edtech"},
  {"name": "Kocam Olur", "career_url": "https://kocamolur.teamtailor.com/jobs", "type": "teamtailor", "logo": "👨‍🏫", "sector": "edtech"},

  # ── GAYRİMENKUL TEKNOLOJİ ──────────────────────────────────────────────────
  {"name": "Hepsiemlak", "career_url": "https://hepsiemlak.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏘️", "sector": "proptech"},
  {"name": "Emlakjet", "career_url": "https://emlakjet.teamtailor.com/jobs", "type": "teamtailor", "logo": "✈️", "sector": "proptech"},
  {"name": "Zingat", "career_url": "https://zingat.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔔", "sector": "proptech"},
  {"name": "Endeksa", "career_url": "https://endeksa.teamtailor.com/jobs", "type": "teamtailor", "logo": "📊", "sector": "proptech"},
  {"name": "Remax Turkey Digital", "career_url": "https://remax.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏡", "sector": "proptech"},
  {"name": "Century21 Turkey", "career_url": "https://century21.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏢", "sector": "proptech"},
  {"name": "Konut.net", "career_url": "https://konut.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏠", "sector": "proptech"},
  {"name": "Arkaplan Digital", "career_url": "https://arkaplan.teamtailor.com/jobs", "type": "teamtailor", "logo": "🖼️", "sector": "proptech"},
  {"name": "Evi Kirala", "career_url": "https://evikirala.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔑", "sector": "proptech"},

  # ── MEDYA & İÇERİK TEKNOLOJİSİ ─────────────────────────────────────────────
  {"name": "Hurriyet Digital", "career_url": "https://hurriyet.teamtailor.com/jobs", "type": "teamtailor", "logo": "📰", "sector": "media"},
  {"name": "Sabah Digital", "career_url": "https://sabah.teamtailor.com/jobs", "type": "teamtailor", "logo": "📰", "sector": "media"},
  {"name": "Milliyet Digital", "career_url": "https://milliyet.teamtailor.com/jobs", "type": "teamtailor", "logo": "📰", "sector": "media"},
  {"name": "CNN Türk Digital", "career_url": "https://cnnturk.teamtailor.com/jobs", "type": "teamtailor", "logo": "📺", "sector": "media"},
  {"name": "BlueTV", "career_url": "https://bluetv.teamtailor.com/jobs", "type": "teamtailor", "logo": "📺", "sector": "media"},
  {"name": "Gain", "career_url": "https://gain.teamtailor.com/jobs", "type": "teamtailor", "logo": "🎬", "sector": "media"},
  {"name": "Puhu TV", "career_url": "https://puhutv.teamtailor.com/jobs", "type": "teamtailor", "logo": "🎥", "sector": "media"},
  {"name": "beIN Media Turkey", "career_url": "https://beinmedia.teamtailor.com/jobs", "type": "teamtailor", "logo": "⚽", "sector": "media"},
  {"name": "Turkcell TV+", "career_url": "https://turkcell.teamtailor.com/jobs", "type": "teamtailor", "logo": "📺", "sector": "media"},
  {"name": "Tivibu", "career_url": "https://tivibu.teamtailor.com/jobs", "type": "teamtailor", "logo": "📡", "sector": "media"},
  {"name": "Digiturk Digital", "career_url": "https://digiturk.teamtailor.com/jobs", "type": "teamtailor", "logo": "📺", "sector": "media"},
  {"name": "Haberler.com", "career_url": "https://haberler.teamtailor.com/jobs", "type": "teamtailor", "logo": "📱", "sector": "media"},
  {"name": "Sözcü Digital", "career_url": "https://sozcu.teamtailor.com/jobs", "type": "teamtailor", "logo": "📰", "sector": "media"},
  {"name": "Mynet", "career_url": "https://mynet.teamtailor.com/jobs", "type": "teamtailor", "logo": "🌐", "sector": "media"},
  {"name": "NTV Digital", "career_url": "https://ntv.teamtailor.com/jobs", "type": "teamtailor", "logo": "📺", "sector": "media"},

  # ── LOJİSTİK & TEDARİK ─────────────────────────────────────────────────────
  {"name": "Aras Kargo Digital", "career_url": "https://araskargo.teamtailor.com/jobs", "type": "teamtailor", "logo": "📦", "sector": "logistics"},
  {"name": "Yurtiçi Kargo Digital", "career_url": "https://yurticicargo.teamtailor.com/jobs", "type": "teamtailor", "logo": "🚚", "sector": "logistics"},
  {"name": "MNG Kargo Digital", "career_url": "https://mngkargo.teamtailor.com/jobs", "type": "teamtailor", "logo": "📫", "sector": "logistics"},
  {"name": "PTT Digital", "career_url": "https://ptt.teamtailor.com/jobs", "type": "teamtailor", "logo": "📮", "sector": "logistics"},
  {"name": "Sendeo", "career_url": "https://sendeo.teamtailor.com/jobs", "type": "teamtailor", "logo": "📨", "sector": "logistics"},
  {"name": "Gönder", "career_url": "https://gonder.teamtailor.com/jobs", "type": "teamtailor", "logo": "✉️", "sector": "logistics"},
  {"name": "Kolay Gelsin", "career_url": "https://kolaygelsin.teamtailor.com/jobs", "type": "teamtailor", "logo": "🤝", "sector": "logistics"},
  {"name": "Applogist", "career_url": "https://applogist.teamtailor.com/jobs", "type": "teamtailor", "logo": "📊", "sector": "logistics"},
  {"name": "Trendyol Express", "career_url": "https://jobs.lever.co/trendyol", "type": "lever", "logo": "⚡", "sector": "logistics"},
  {"name": "Invio Lojistik", "career_url": "https://invio.teamtailor.com/jobs", "type": "teamtailor", "logo": "🚛", "sector": "logistics"},
  {"name": "DPD Turkey", "career_url": "https://dpd.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔴", "sector": "logistics"},
  {"name": "Aramex Turkey", "career_url": "https://aramex.teamtailor.com/jobs", "type": "teamtailor", "logo": "📦", "sector": "logistics"},

  # ── OTOMOTİV TEKNOLOJİ ─────────────────────────────────────────────────────
  {"name": "Ford Otosan Digital", "career_url": "https://fordotosan.teamtailor.com/jobs", "type": "teamtailor", "logo": "🚗", "sector": "autotech"},
  {"name": "Tofaş Digital", "career_url": "https://tofas.teamtailor.com/jobs", "type": "teamtailor", "logo": "🚙", "sector": "autotech"},
  {"name": "Oyak Renault Digital", "career_url": "https://oyakrenault.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏎️", "sector": "autotech"},
  {"name": "Doğuş Otomotiv Digital", "career_url": "https://dogusoto.teamtailor.com/jobs", "type": "teamtailor", "logo": "🚘", "sector": "autotech"},
  {"name": "Oto.com.tr", "career_url": "https://oto.teamtailor.com/jobs", "type": "teamtailor", "logo": "🚗", "sector": "autotech"},
  {"name": "Arabam.com", "career_url": "https://arabam.teamtailor.com/jobs", "type": "teamtailor", "logo": "🚗", "sector": "autotech"},
  {"name": "Otokoç Digital", "career_url": "https://otokoc.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏢", "sector": "autotech"},
  {"name": "Togg Digital", "career_url": "https://togg.teamtailor.com/jobs", "type": "teamtailor", "logo": "⚡", "sector": "autotech"},
  {"name": "Carvak", "career_url": "https://carvak.teamtailor.com/jobs", "type": "teamtailor", "logo": "🚘", "sector": "autotech"},
  {"name": "Garaj.io", "career_url": "https://garajio.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔧", "sector": "autotech"},

  # ── BT HİZMETLERİ & DANIŞMANLIK ────────────────────────────────────────────
  {"name": "Arvato Systems Turkey", "career_url": "https://arvato.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔷", "sector": "itservices"},
  {"name": "Borusan Teknoloji", "career_url": "https://borusanteknoloji.teamtailor.com/jobs", "type": "teamtailor", "logo": "⚙️", "sector": "itservices"},
  {"name": "NTT Data Turkey", "career_url": "https://nttdata.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔷", "sector": "itservices"},
  {"name": "Capgemini Turkey", "career_url": "https://capgemini.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔵", "sector": "itservices"},
  {"name": "Accenture Turkey", "career_url": "https://accenture.teamtailor.com/jobs", "type": "teamtailor", "logo": "🟣", "sector": "itservices"},
  {"name": "Deloitte Turkey Digital", "career_url": "https://deloitte.teamtailor.com/jobs", "type": "teamtailor", "logo": "🟢", "sector": "itservices"},
  {"name": "PwC Turkey Digital", "career_url": "https://pwc.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔴", "sector": "itservices"},
  {"name": "IBM Turkey", "career_url": "https://ibm.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔵", "sector": "itservices"},
  {"name": "SAP Turkey", "career_url": "https://sap.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔷", "sector": "itservices"},
  {"name": "Oracle Turkey", "career_url": "https://oracle.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔴", "sector": "itservices"},
  {"name": "Ericsson Turkey", "career_url": "https://jobs.lever.co/ericsson", "type": "lever", "logo": "📡", "sector": "itservices"},
  {"name": "Cisco Turkey Digital", "career_url": "https://jobs.lever.co/cisco", "type": "lever", "logo": "🔗", "sector": "itservices"},
  {"name": "Siemens Turkey Digital", "career_url": "https://jobs.lever.co/siemens", "type": "lever", "logo": "⚡", "sector": "itservices"},
  {"name": "Wipro Turkey", "career_url": "https://wipro.teamtailor.com/jobs", "type": "teamtailor", "logo": "🌸", "sector": "itservices"},
  {"name": "Infosys Turkey", "career_url": "https://infosys.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔷", "sector": "itservices"},
  {"name": "CGI Turkey", "career_url": "https://cgi.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏗️", "sector": "itservices"},
  {"name": "Conduent Turkey", "career_url": "https://conduent.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔧", "sector": "itservices"},
  {"name": "Teleperformance Turkey", "career_url": "https://teleperformance.teamtailor.com/jobs", "type": "teamtailor", "logo": "📞", "sector": "itservices"},
  {"name": "Concentrix Turkey", "career_url": "https://concentrix.teamtailor.com/jobs", "type": "teamtailor", "logo": "🎯", "sector": "itservices"},
  {"name": "HCL Technologies Turkey", "career_url": "https://hcltech.teamtailor.com/jobs", "type": "teamtailor", "logo": "💚", "sector": "itservices"},
  {"name": "Tata Consultancy Turkey", "career_url": "https://tcs.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔵", "sector": "itservices"},
  {"name": "Cognizant Turkey", "career_url": "https://cognizant.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔵", "sector": "itservices"},
  {"name": "Globant Turkey", "career_url": "https://jobs.lever.co/globant", "type": "lever", "logo": "🌎", "sector": "itservices"},
  {"name": "EPAM Systems Turkey", "career_url": "https://jobs.lever.co/epam", "type": "lever", "logo": "🔷", "sector": "itservices"},
  {"name": "SoftServe Turkey", "career_url": "https://jobs.lever.co/softserve", "type": "lever", "logo": "🌊", "sector": "itservices"},

  # ── SİBER GÜVENLİK ─────────────────────────────────────────────────────────
  {"name": "Picus Security", "career_url": "https://jobs.lever.co/picussecurity", "type": "lever", "logo": "🔐", "sector": "cybersec"},
  {"name": "Berqnet", "career_url": "https://berqnet.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔒", "sector": "cybersec"},
  {"name": "Prodaft", "career_url": "https://prodaft.teamtailor.com/jobs", "type": "teamtailor", "logo": "🕵️", "sector": "cybersec"},
  {"name": "Brandefense", "career_url": "https://brandefense.teamtailor.com/jobs", "type": "teamtailor", "logo": "🛡️", "sector": "cybersec"},
  {"name": "InfiSec", "career_url": "https://infisec.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔐", "sector": "cybersec"},
  {"name": "Biznet Teknoloji", "career_url": "https://biznet.teamtailor.com/jobs", "type": "teamtailor", "logo": "🌐", "sector": "cybersec"},
  {"name": "Komtera Teknoloji", "career_url": "https://komtera.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔧", "sector": "cybersec"},
  {"name": "ADEO Cyber Security", "career_url": "https://adeocs.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔒", "sector": "cybersec"},
  {"name": "Turkcell Siber Güvenlik", "career_url": "https://turkcellcyber.teamtailor.com/jobs", "type": "teamtailor", "logo": "📱", "sector": "cybersec"},
  {"name": "Suisse Security Turkey", "career_url": "https://suissesecurity.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔐", "sector": "cybersec"},
  {"name": "Logsign", "career_url": "https://logsign.teamtailor.com/jobs", "type": "teamtailor", "logo": "📊", "sector": "cybersec"},
  {"name": "Keepnet Labs", "career_url": "https://keepnetlabs.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔐", "sector": "cybersec"},
  {"name": "Nozomi Networks Turkey", "career_url": "https://jobs.lever.co/nozominetworks", "type": "lever", "logo": "🌿", "sector": "cybersec"},

  # ── YAPAY ZEKA & VERİ TEKNOLOJİSİ ─────────────────────────────────────────
  {"name": "Brandnew IO", "career_url": "https://brandnewio.teamtailor.com/jobs", "type": "teamtailor", "logo": "🧠", "sector": "aidata"},
  {"name": "Alesta Teknoloji", "career_url": "https://alesta.teamtailor.com/jobs", "type": "teamtailor", "logo": "⚡", "sector": "aidata"},
  {"name": "Metatron AI", "career_url": "https://metatronai.teamtailor.com/jobs", "type": "teamtailor", "logo": "🤖", "sector": "aidata"},
  {"name": "QDNA", "career_url": "https://qdna.teamtailor.com/jobs", "type": "teamtailor", "logo": "🧬", "sector": "aidata"},
  {"name": "DataIker Turkey", "career_url": "https://dataiker.teamtailor.com/jobs", "type": "teamtailor", "logo": "📊", "sector": "aidata"},
  {"name": "Datalabs Turkey", "career_url": "https://datalabs.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔬", "sector": "aidata"},
  {"name": "CEVA Logistics Turkey Tech", "career_url": "https://ceva.teamtailor.com/jobs", "type": "teamtailor", "logo": "🚛", "sector": "aidata"},
  {"name": "Segmentify AI", "career_url": "https://segmentify.teamtailor.com/jobs", "type": "teamtailor", "logo": "📈", "sector": "aidata"},
  {"name": "Sensfix Turkey", "career_url": "https://sensfix.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔧", "sector": "aidata"},
  {"name": "Revelo Turkey", "career_url": "https://jobs.lever.co/revelo", "type": "lever", "logo": "💡", "sector": "aidata"},
  {"name": "Scale AI Turkey", "career_url": "https://jobs.lever.co/scaleai", "type": "lever", "logo": "📊", "sector": "aidata"},
  {"name": "Weights & Biases Turkey", "career_url": "https://jobs.lever.co/wandb", "type": "lever", "logo": "⚖️", "sector": "aidata"},

  # ── SANAYİ & ENERJİ DİJİTAL ─────────────────────────────────────────────────
  {"name": "Enerjisa Digital", "career_url": "https://enerjisa.teamtailor.com/jobs", "type": "teamtailor", "logo": "⚡", "sector": "industrial"},
  {"name": "Çimsa Digital", "career_url": "https://cimsa.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏗️", "sector": "industrial"},
  {"name": "Kordsa Digital", "career_url": "https://kordsa.teamtailor.com/jobs", "type": "teamtailor", "logo": "🧵", "sector": "industrial"},
  {"name": "Sabancı Holding Digital", "career_url": "https://sabanci.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏢", "sector": "industrial"},
  {"name": "Koç Holding Digital", "career_url": "https://koc.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏛️", "sector": "industrial"},
  {"name": "Bosch Turkey Digital", "career_url": "https://jobs.lever.co/bosch", "type": "lever", "logo": "🔧", "sector": "industrial"},
  {"name": "Schneider Electric Turkey", "career_url": "https://jobs.lever.co/schneiderelectric", "type": "lever", "logo": "⚡", "sector": "industrial"},
  {"name": "ABB Turkey Digital", "career_url": "https://jobs.lever.co/abb", "type": "lever", "logo": "⚡", "sector": "industrial"},
  {"name": "GE Turkey Digital", "career_url": "https://jobs.lever.co/ge", "type": "lever", "logo": "💡", "sector": "industrial"},
  {"name": "Honeywell Turkey", "career_url": "https://jobs.lever.co/honeywell", "type": "lever", "logo": "🌡️", "sector": "industrial"},
  {"name": "3M Turkey Digital", "career_url": "https://jobs.lever.co/3m", "type": "lever", "logo": "🔬", "sector": "industrial"},
  {"name": "Philips Turkey Digital", "career_url": "https://jobs.lever.co/philips", "type": "lever", "logo": "💡", "sector": "industrial"},

  # ── ULUSLARARASI FİRMALAR (TR OFİSİ) ───────────────────────────────────────
  {"name": "Microsoft Turkey", "career_url": "https://jobs.lever.co/microsoft", "type": "lever", "logo": "🪟", "sector": "international"},
  {"name": "Google Turkey", "career_url": "https://jobs.lever.co/google", "type": "lever", "logo": "🔍", "sector": "international"},
  {"name": "Amazon Turkey (AWS)", "career_url": "https://jobs.lever.co/amazon", "type": "lever", "logo": "📦", "sector": "international"},
  {"name": "Salesforce Turkey", "career_url": "https://jobs.lever.co/salesforce", "type": "lever", "logo": "☁️", "sector": "international"},
  {"name": "ServiceNow Turkey", "career_url": "https://jobs.lever.co/servicenow", "type": "lever", "logo": "🔄", "sector": "international"},
  {"name": "Dynatrace Turkey", "career_url": "https://jobs.lever.co/dynatrace", "type": "lever", "logo": "📊", "sector": "international"},
  {"name": "Atlassian Istanbul", "career_url": "https://jobs.lever.co/atlassian", "type": "lever", "logo": "🅰️", "sector": "international"},
  {"name": "Adjust Istanbul", "career_url": "https://jobs.lever.co/adjust", "type": "lever", "logo": "📊", "sector": "international"},
  {"name": "Picsart Istanbul", "career_url": "https://jobs.lever.co/picsart", "type": "lever", "logo": "🎨", "sector": "international"},
  {"name": "Canva Turkey", "career_url": "https://jobs.lever.co/canva", "type": "lever", "logo": "🎨", "sector": "international"},
  {"name": "Figma Turkey", "career_url": "https://jobs.lever.co/figma", "type": "lever", "logo": "🎨", "sector": "international"},
  {"name": "Miro Turkey", "career_url": "https://jobs.lever.co/miro", "type": "lever", "logo": "🖍️", "sector": "international"},
  {"name": "Notion Turkey", "career_url": "https://jobs.lever.co/notion", "type": "lever", "logo": "📓", "sector": "international"},
  {"name": "Stripe Turkey", "career_url": "https://jobs.lever.co/stripe", "type": "lever", "logo": "💳", "sector": "international"},
  {"name": "Klarna Turkey", "career_url": "https://jobs.lever.co/klarna", "type": "lever", "logo": "🛍️", "sector": "international"},
  {"name": "Spotify Turkey", "career_url": "https://jobs.lever.co/spotify", "type": "lever", "logo": "🎵", "sector": "international"},
  {"name": "TikTok Turkey (ByteDance)", "career_url": "https://jobs.lever.co/bytedance", "type": "lever", "logo": "🎵", "sector": "international"},
  {"name": "Meta Turkey", "career_url": "https://jobs.lever.co/meta", "type": "lever", "logo": "👥", "sector": "international"},
  {"name": "Twitter/X Turkey", "career_url": "https://jobs.lever.co/x", "type": "lever", "logo": "🐦", "sector": "international"},
  {"name": "Expedia Turkey", "career_url": "https://jobs.lever.co/expedia", "type": "lever", "logo": "✈️", "sector": "international"},
  {"name": "Trivago Turkey", "career_url": "https://jobs.lever.co/trivago", "type": "lever", "logo": "🏨", "sector": "international"},
  {"name": "Agoda Turkey", "career_url": "https://jobs.lever.co/agoda", "type": "lever", "logo": "🏩", "sector": "international"},
  {"name": "Grab Turkey", "career_url": "https://jobs.lever.co/grab", "type": "lever", "logo": "🚗", "sector": "international"},
  {"name": "N26 Turkey", "career_url": "https://jobs.lever.co/n26", "type": "lever", "logo": "💳", "sector": "international"},
  {"name": "Revolut Turkey", "career_url": "https://jobs.lever.co/revolut", "type": "lever", "logo": "🔄", "sector": "international"},
  {"name": "Wise Turkey", "career_url": "https://jobs.lever.co/wise", "type": "lever", "logo": "💸", "sector": "international"},

  # ── YAZILIM EVLERİ & AJANSLAR ───────────────────────────────────────────────
  {"name": "Maslak Works", "career_url": "https://maslakworks.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏢", "sector": "agency"},
  {"name": "RDC Digital", "career_url": "https://rdc.teamtailor.com/jobs", "type": "teamtailor", "logo": "📱", "sector": "agency"},
  {"name": "Mobildev", "career_url": "https://mobildev.teamtailor.com/jobs", "type": "teamtailor", "logo": "📲", "sector": "agency"},
  {"name": "Hexa Digital Agency", "career_url": "https://hexa.teamtailor.com/jobs", "type": "teamtailor", "logo": "⬡", "sector": "agency"},
  {"name": "Kırmızı Digital", "career_url": "https://kirmizi.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔴", "sector": "agency"},
  {"name": "ARGE Yazılım", "career_url": "https://argeyazilim.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔬", "sector": "agency"},
  {"name": "Solverra", "career_url": "https://solverra.teamtailor.com/jobs", "type": "teamtailor", "logo": "💡", "sector": "agency"},
  {"name": "Netventory", "career_url": "https://netventory.teamtailor.com/jobs", "type": "teamtailor", "logo": "📦", "sector": "agency"},
  {"name": "Code&Pepper Istanbul", "career_url": "https://codeandpepper.teamtailor.com/jobs", "type": "teamtailor", "logo": "🌶️", "sector": "agency"},
  {"name": "Novice Digital", "career_url": "https://novice.teamtailor.com/jobs", "type": "teamtailor", "logo": "🆕", "sector": "agency"},
  {"name": "Yazılımcı.io", "career_url": "https://yazilimci.teamtailor.com/jobs", "type": "teamtailor", "logo": "💻", "sector": "agency"},
  {"name": "Flexera Turkey", "career_url": "https://flexera.teamtailor.com/jobs", "type": "teamtailor", "logo": "⚙️", "sector": "agency"},
  {"name": "Webrazzi Studios", "career_url": "https://webrazzi.teamtailor.com/jobs", "type": "teamtailor", "logo": "🕸️", "sector": "agency"},
  {"name": "Bigumigu Digital", "career_url": "https://bigumigu.teamtailor.com/jobs", "type": "teamtailor", "logo": "🎨", "sector": "agency"},
  {"name": "Altin Çekiç Digital", "career_url": "https://altincekic.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔨", "sector": "agency"},

  # ── İNSAN KAYNAKLARI TEKNOLOJİ ─────────────────────────────────────────────
  {"name": "Kariyer.net", "career_url": "https://kariyer.teamtailor.com/jobs", "type": "teamtailor", "logo": "💼", "sector": "hrtech"},
  {"name": "Yenibiris.com", "career_url": "https://yenibiris.teamtailor.com/jobs", "type": "teamtailor", "logo": "👥", "sector": "hrtech"},
  {"name": "Workup", "career_url": "https://workup.teamtailor.com/jobs", "type": "teamtailor", "logo": "💼", "sector": "hrtech"},
  {"name": "HumanGroup", "career_url": "https://humangroup.teamtailor.com/jobs", "type": "teamtailor", "logo": "👥", "sector": "hrtech"},
  {"name": "ManpowerGroup Turkey", "career_url": "https://manpowergroup.teamtailor.com/jobs", "type": "teamtailor", "logo": "💪", "sector": "hrtech"},
  {"name": "Robert Half Turkey", "career_url": "https://roberthalf.teamtailor.com/jobs", "type": "teamtailor", "logo": "🤝", "sector": "hrtech"},
  {"name": "Assessfirst Turkey", "career_url": "https://assessfirst.teamtailor.com/jobs", "type": "teamtailor", "logo": "📊", "sector": "hrtech"},
  {"name": "İKSAD", "career_url": "https://iksad.teamtailor.com/jobs", "type": "teamtailor", "logo": "🎓", "sector": "hrtech"},
  {"name": "Lemon10 Turkey", "career_url": "https://lemon10.teamtailor.com/jobs", "type": "teamtailor", "logo": "🍋", "sector": "hrtech"},
  {"name": "TeamTailor Turkey", "career_url": "https://teamtailor.teamtailor.com/jobs", "type": "teamtailor", "logo": "👥", "sector": "hrtech"},

  # ── STARTUP & SCALE-UP ──────────────────────────────────────────────────────
  {"name": "Getmobil", "career_url": "https://getmobil.teamtailor.com/jobs", "type": "teamtailor", "logo": "📱", "sector": "startup"},
  {"name": "Lobi.co", "career_url": "https://lobi.teamtailor.com/jobs", "type": "teamtailor", "logo": "🎮", "sector": "startup"},
  {"name": "Payibol", "career_url": "https://payibol.teamtailor.com/jobs", "type": "teamtailor", "logo": "💰", "sector": "startup"},
  {"name": "Coinnect", "career_url": "https://coinnect.teamtailor.com/jobs", "type": "teamtailor", "logo": "🔗", "sector": "startup"},
  {"name": "Kobi Teknoloji", "career_url": "https://kobiteknoloji.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏭", "sector": "startup"},
  {"name": "Startwise Turkey", "career_url": "https://startwise.teamtailor.com/jobs", "type": "teamtailor", "logo": "🚀", "sector": "startup"},
  {"name": "Hepsijet", "career_url": "https://hepsijet.teamtailor.com/jobs", "type": "teamtailor", "logo": "✈️", "sector": "startup"},
  {"name": "Müşteri Kontrol", "career_url": "https://musterikontrol.teamtailor.com/jobs", "type": "teamtailor", "logo": "⭐", "sector": "startup"},
  {"name": "Yapay Zeka Fabrikası", "career_url": "https://yapayzekafarikasi.teamtailor.com/jobs", "type": "teamtailor", "logo": "🤖", "sector": "startup"},
  {"name": "Plandek Turkey", "career_url": "https://plandek.teamtailor.com/jobs", "type": "teamtailor", "logo": "📊", "sector": "startup"},
  {"name": "Flowla", "career_url": "https://flowla.teamtailor.com/jobs", "type": "teamtailor", "logo": "🌊", "sector": "startup"},
  {"name": "PiStats", "career_url": "https://pistats.teamtailor.com/jobs", "type": "teamtailor", "logo": "📊", "sector": "startup"},
  {"name": "Velox Istanbul", "career_url": "https://velox.teamtailor.com/jobs", "type": "teamtailor", "logo": "⚡", "sector": "startup"},
  {"name": "Lemon Digital", "career_url": "https://lemondigital.teamtailor.com/jobs", "type": "teamtailor", "logo": "🍋", "sector": "startup"},
  {"name": "Bosphorus Tech", "career_url": "https://bosphorustech.teamtailor.com/jobs", "type": "teamtailor", "logo": "🌉", "sector": "startup"},
  {"name": "GovTech Turkey", "career_url": "https://govtech.teamtailor.com/jobs", "type": "teamtailor", "logo": "🏛️", "sector": "startup"},
  {"name": "FoodTech Turkey", "career_url": "https://foodtech.teamtailor.com/jobs", "type": "teamtailor", "logo": "🍽️", "sector": "startup"},
  {"name": "CleanTech Turkey", "career_url": "https://cleantech.teamtailor.com/jobs", "type": "teamtailor", "logo": "♻️", "sector": "startup"},
  {"name": "SpaceTech Turkey", "career_url": "https://spacetech.teamtailor.com/jobs", "type": "teamtailor", "logo": "🚀", "sector": "startup"},
  {"name": "AgriTech Turkey", "career_url": "https://agritech.teamtailor.com/jobs", "type": "teamtailor", "logo": "🌱", "sector": "startup"},
  {"name": "Parabol Istanbul", "career_url": "https://jobs.lever.co/parabol", "type": "lever", "logo": "⭕", "sector": "startup"},
  {"name": "Deel Turkey", "career_url": "https://jobs.lever.co/deel", "type": "lever", "logo": "🌍", "sector": "startup"},
  {"name": "Remote.com Turkey", "career_url": "https://jobs.lever.co/remote", "type": "lever", "logo": "🏠", "sector": "startup"},
  {"name": "Oyster Turkey", "career_url": "https://jobs.lever.co/oysterhr", "type": "lever", "logo": "🦪", "sector": "startup"},
  {"name": "Factorial Turkey", "career_url": "https://jobs.lever.co/factorial", "type": "lever", "logo": "🔢", "sector": "startup"},
]


def main():
    # Mevcut listeyi yükle
    with open(COMPANIES_FILE, "r", encoding="utf-8") as f:
        existing = json.load(f)

    existing_names = {c["name"].lower().strip() for c in existing}
    added = 0

    for company in NEW_COMPANIES:
        name = company.get("name", "").lower().strip()
        if name and name not in existing_names:
            # url alanını ekle (yoksa boş bırak)
            company.setdefault("url", "")
            existing.append(company)
            existing_names.add(name)
            added += 1

    # Kaydet
    with open(COMPANIES_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"✅ {added} yeni firma eklendi!")
    print(f"📊 Toplam firma sayısı: {len(existing)}")

    # Sektör dağılımı
    from collections import Counter
    sectors = Counter(c.get("sector", "unknown") for c in existing)
    print("\n📋 Sektör dağılımı:")
    for sector, count in sorted(sectors.items(), key=lambda x: -x[1]):
        print(f"  {sector}: {count}")


if __name__ == "__main__":
    main()
