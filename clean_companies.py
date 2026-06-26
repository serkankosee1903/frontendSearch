#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
companies.json'u temizler:
- Tahmin edilen teamtailor/lever URL'lerini kaldırır
- Sadece gerçek website URL'lerini tutar
- smart_scraper.py bu websiteleri ziyaret edip kariyer sayfasını bulacak
"""

import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
FILE = SCRIPT_DIR / "companies.json"

# ─── Gerçek website URL'leri olan firmalar ─────────────────────────────────────
# Sadece name + gerçek url + logo. career_url yok, type yok.
# smart_scraper.py her firmanın sitesine gidip kariyer sayfasını otomatik bulacak.

CLEAN_COMPANIES = [

  # ── E-TİCARET & MARKETPLACEhttps ───────────────────────────────────────────
  {"name": "Trendyol",               "url": "https://www.trendyol.com",            "logo": "🛒"},
  {"name": "Hepsiburada",            "url": "https://www.hepsiburada.com",          "logo": "🛍️"},
  {"name": "Getir",                  "url": "https://getir.com",                    "logo": "🚀"},
  {"name": "Yemeksepeti",            "url": "https://www.yemeksepeti.com",          "logo": "🍕"},
  {"name": "Sahibinden",             "url": "https://www.sahibinden.com",           "logo": "🏠"},
  {"name": "n11",                    "url": "https://www.n11.com",                  "logo": "🛒"},
  {"name": "GittiGidiyor",           "url": "https://www.gittigidiyor.com",         "logo": "🛒"},
  {"name": "Çiçeksepeti",            "url": "https://www.ciceksepeti.com",          "logo": "🌸"},
  {"name": "Modanisa",               "url": "https://www.modanisa.com",             "logo": "👗"},
  {"name": "Dolap",                  "url": "https://dolap.com",                    "logo": "👕"},
  {"name": "Flo",                    "url": "https://www.flo.com.tr",               "logo": "👟"},
  {"name": "LC Waikiki",             "url": "https://www.lcwaikiki.com",            "logo": "👕"},
  {"name": "Mavi Jeans",             "url": "https://www.mavi.com",                 "logo": "👖"},
  {"name": "Koton",                  "url": "https://www.koton.com",                "logo": "👗"},
  {"name": "DeFacto",                "url": "https://www.defacto.com.tr",           "logo": "🧥"},
  {"name": "Boyner",                 "url": "https://www.boyner.com.tr",            "logo": "👔"},
  {"name": "Beymen",                 "url": "https://www.beymen.com",               "logo": "👒"},
  {"name": "Akinon",                 "url": "https://akinon.com",                   "logo": "🛍️"},
  {"name": "ikas",                   "url": "https://ikas.com",                     "logo": "🛍️"},
  {"name": "Tazedirekt",             "url": "https://www.tazedirekt.com",           "logo": "🥑"},
  {"name": "Teknosa",                "url": "https://www.teknosa.com",              "logo": "🖥️"},
  {"name": "Vatan Bilgisayar",       "url": "https://www.vatanbilgisayar.com",      "logo": "💻"},
  {"name": "MediaMarkt Turkey",      "url": "https://www.mediamarkt.com.tr",        "logo": "📺"},
  {"name": "Hepsijet",               "url": "https://www.hepsijet.com",             "logo": "📦"},
  {"name": "Gratis",                 "url": "https://www.gratis.com",               "logo": "💄"},
  {"name": "Watsons Turkey",         "url": "https://www.watsons.com.tr",           "logo": "🧴"},
  {"name": "Ebebek",                 "url": "https://www.ebebek.com",               "logo": "🍼"},
  {"name": "D&R",                    "url": "https://www.dr.com.tr",                "logo": "📚"},
  {"name": "Morhipo",                "url": "https://www.morhipo.com",              "logo": "👗"},
  {"name": "Shopiverse",             "url": "https://shopiverse.com",               "logo": "🛍️"},

  # ── FİNTECH & ÖDEME SİSTEMLERİ ─────────────────────────────────────────────
  {"name": "Papara",                 "url": "https://www.papara.com",               "logo": "💳"},
  {"name": "iyzico",                 "url": "https://www.iyzico.com",               "logo": "💰"},
  {"name": "PayTR",                  "url": "https://www.paytr.com",                "logo": "💳"},
  {"name": "Sipay",                  "url": "https://www.sipay.com.tr",             "logo": "💱"},
  {"name": "Param",                  "url": "https://param.com.tr",                 "logo": "💰"},
  {"name": "Tosla",                  "url": "https://tosla.com",                    "logo": "💸"},
  {"name": "Ininal",                 "url": "https://www.ininal.com",               "logo": "💳"},
  {"name": "Craftgate",              "url": "https://craftgate.io",                 "logo": "💳"},
  {"name": "BtcTurk",               "url": "https://www.btcturk.com",              "logo": "₿"},
  {"name": "Paribu",                 "url": "https://www.paribu.com",               "logo": "💹"},
  {"name": "Bitexen",                "url": "https://bitexen.com",                  "logo": "₿"},
  {"name": "Icrypex",                "url": "https://www.icrypex.com",              "logo": "🔐"},
  {"name": "Colendi",                "url": "https://colendi.com",                  "logo": "💰"},
  {"name": "Paycell",                "url": "https://paycell.com.tr",               "logo": "💳"},
  {"name": "Hopi",                   "url": "https://hopi.com.tr",                  "logo": "🎁"},
  {"name": "Paraşüt",                "url": "https://parasut.com",                  "logo": "📋"},
  {"name": "Token Finansal Teknoloji","url": "https://www.token.com.tr",             "logo": "🔑"},
  {"name": "Vepara",                 "url": "https://www.vepara.com.tr",            "logo": "💳"},
  {"name": "Lidio",                  "url": "https://lidio.com",                    "logo": "💰"},
  {"name": "Hayat Finans",           "url": "https://www.hayatfinans.com.tr",       "logo": "💰"},

  # ── BANKACILIK & SİGORTA TEKNOLOJİ ─────────────────────────────────────────
  {"name": "Garanti BBVA Teknoloji", "url": "https://www.garantibbvateknoloji.com.tr","logo": "💳"},
  {"name": "Yapı Kredi Teknoloji",   "url": "https://www.ykteknoloji.com.tr",       "logo": "🏛️"},
  {"name": "İştech",                 "url": "https://www.istech.com.tr",            "logo": "🏦"},
  {"name": "Softtech",               "url": "https://www.softtech.com.tr",          "logo": "🏦"},
  {"name": "Intertech",              "url": "https://www.intertech.com.tr",         "logo": "💻"},
  {"name": "Ziraat Teknoloji",       "url": "https://www.ziraatteknoloji.com",      "logo": "🌾"},
  {"name": "Akbank",                 "url": "https://www.akbank.com",               "logo": "🏦"},
  {"name": "ING Turkey",             "url": "https://www.ing.com.tr",               "logo": "🏦"},
  {"name": "Fibabanka",              "url": "https://www.fibabanka.com.tr",          "logo": "🏦"},
  {"name": "Denizbank",              "url": "https://www.denizbank.com",             "logo": "🏦"},
  {"name": "TEB Teknoloji",          "url": "https://www.teb.com.tr",               "logo": "🏦"},
  {"name": "Odeabank",               "url": "https://www.odeabank.com.tr",           "logo": "🏦"},
  {"name": "Albaraka Türk",          "url": "https://www.albarakaturk.com.tr",      "logo": "🏦"},
  {"name": "Kuveyt Türk",            "url": "https://www.kuveytturk.com.tr",        "logo": "🏦"},
  {"name": "Vakıfbank Teknoloji",    "url": "https://www.vakifbankteknoloji.com.tr","logo": "🏦"},
  {"name": "Halkbank Teknoloji",     "url": "https://www.halkbankteknoloji.com.tr", "logo": "🏦"},
  {"name": "Sigortam.net",           "url": "https://www.sigortam.net",             "logo": "🛡️"},
  {"name": "Aksigorta",              "url": "https://www.aksigorta.com.tr",         "logo": "🛡️"},
  {"name": "Allianz Türkiye",        "url": "https://www.allianz.com.tr",           "logo": "🔵"},
  {"name": "Anadolu Sigorta",        "url": "https://www.anadolusigorta.com.tr",    "logo": "🛡️"},
  {"name": "Avivasa",                "url": "https://www.avivasa.com.tr",           "logo": "🛡️"},

  # ── TELEKOMÜNİKASYON ────────────────────────────────────────────────────────
  {"name": "Turkcell",               "url": "https://www.turkcell.com.tr",          "logo": "📱"},
  {"name": "Turkcell Teknoloji",     "url": "https://turkcellteknoloji.com.tr",     "logo": "📡"},
  {"name": "TT Teknoloji",           "url": "https://ttteknoloji.com.tr",           "logo": "📞"},
  {"name": "Türk Telekom",           "url": "https://www.turktelekom.com.tr",       "logo": "📶"},
  {"name": "Vodafone Turkey",        "url": "https://www.vodafone.com.tr",          "logo": "📶"},
  {"name": "Superonline",            "url": "https://www.superonline.net",          "logo": "🌐"},
  {"name": "TurkNet",                "url": "https://www.turknet.net.tr",           "logo": "🌐"},
  {"name": "BiP",                    "url": "https://bip.com.tr",                   "logo": "💬"},
  {"name": "Türksat",                "url": "https://www.turksat.com.tr",           "logo": "🛰️"},
  {"name": "Global Bilgi",           "url": "https://www.globalbilgi.com.tr",       "logo": "🌍"},
  {"name": "Millenicom",             "url": "https://www.millenicom.com.tr",        "logo": "📡"},

  # ── OYUN & EĞLENCE ──────────────────────────────────────────────────────────
  {"name": "Dream Games",            "url": "https://www.dreamgames.com",           "logo": "🎯"},
  {"name": "Peak Games",             "url": "https://www.peakgames.net",            "logo": "🎮"},
  {"name": "Spyke Games",            "url": "https://www.spykegames.com",           "logo": "🎮"},
  {"name": "Rollic Games",           "url": "https://rollic.games",                 "logo": "🎲"},
  {"name": "Gram Games",             "url": "https://www.gramgames.com",            "logo": "🎯"},
  {"name": "Masomo",                 "url": "https://masomo.com",                   "logo": "⚽"},
  {"name": "Bigger Games",           "url": "https://www.biggergames.com",          "logo": "🎮"},
  {"name": "Codeway",                "url": "https://codeway.co",                   "logo": "📱"},
  {"name": "Good Job Games",         "url": "https://goodjobgames.com",             "logo": "✅"},
  {"name": "Fugo Games",             "url": "https://fugogames.com",                "logo": "🎮"},
  {"name": "Joygame",                "url": "https://www.joygame.com",              "logo": "😄"},
  {"name": "Nays Games",             "url": "https://nays.com.tr",                  "logo": "🎮"},
  {"name": "Coda Platform",          "url": "https://www.codaplatform.com",         "logo": "🎮"},
  {"name": "Plarium",                "url": "https://plarium.com",                  "logo": "⚔️"},
  {"name": "Zynga Istanbul",         "url": "https://www.zynga.com",                "logo": "🃏"},
  {"name": "Supercell",              "url": "https://supercell.com",                "logo": "🏆"},

  # ── KURUMSAL YAZILIM & SaaS ──────────────────────────────────────────────────
  {"name": "Logo Yazılım",           "url": "https://www.logo.com.tr",              "logo": "💼"},
  {"name": "Insider",                "url": "https://useinsider.com",               "logo": "📊"},
  {"name": "Segmentify",             "url": "https://www.segmentify.com",           "logo": "📈"},
  {"name": "UserGuiding",            "url": "https://userguiding.com",              "logo": "👥"},
  {"name": "Prisync",                "url": "https://prisync.com",                  "logo": "📊"},
  {"name": "Storyly",                "url": "https://storyly.io",                   "logo": "📖"},
  {"name": "Jotform",                "url": "https://www.jotform.com",              "logo": "📝"},
  {"name": "Testinium",              "url": "https://testinium.com",                "logo": "🧪"},
  {"name": "Appcircle",              "url": "https://appcircle.io",                 "logo": "⭕"},
  {"name": "Vispera",                "url": "https://vispera.co",                   "logo": "👁️"},
  {"name": "Bimser",                 "url": "https://www.bimser.com.tr",            "logo": "⚙️"},
  {"name": "IdeaSoft",               "url": "https://www.ideasoft.com.tr",          "logo": "💡"},
  {"name": "Netmera",                "url": "https://netmera.com",                  "logo": "📱"},
  {"name": "NetGSM",                 "url": "https://www.netgsm.com.tr",            "logo": "📱"},
  {"name": "Mikro Yazılım",          "url": "https://www.mikro.com.tr",             "logo": "📊"},
  {"name": "Netsis",                 "url": "https://www.netsis.com.tr",            "logo": "💾"},
  {"name": "Uyumsoft",               "url": "https://www.uyumsoft.com.tr",          "logo": "📖"},
  {"name": "Apsiyon",                "url": "https://apsiyon.com",                  "logo": "🏠"},

  # ── SİBER GÜVENLİK ──────────────────────────────────────────────────────────
  {"name": "Picus Security",         "url": "https://www.picussecurity.com",        "logo": "🔐"},
  {"name": "Berqnet",                "url": "https://www.berqnet.com",              "logo": "🔒"},
  {"name": "Logsign",                "url": "https://www.logsign.com",              "logo": "📊"},
  {"name": "Keepnet Labs",           "url": "https://keepnetlabs.com",              "logo": "🔐"},
  {"name": "Prodaft",                "url": "https://www.prodaft.com",              "logo": "🕵️"},
  {"name": "Biges",                  "url": "https://biges.com",                    "logo": "🔐"},
  {"name": "Cybersoft",              "url": "https://cybersoft.com.tr",             "logo": "🛡️"},
  {"name": "Brandefense",            "url": "https://brandefense.io",               "logo": "🛡️"},
  {"name": "Biznet Teknoloji",       "url": "https://www.biznet.com.tr",            "logo": "🌐"},

  # ── IT HİZMETLERİ & DANIŞMANLIK ─────────────────────────────────────────────
  {"name": "KoçSistem",              "url": "https://www.kocsistem.com.tr",         "logo": "🏢"},
  {"name": "Doğuş Teknoloji",        "url": "https://www.dogusteknoloji.com",       "logo": "🏢"},
  {"name": "Etiya",                  "url": "https://www.etiya.com",                "logo": "🔷"},
  {"name": "Innova",                 "url": "https://www.innova.com.tr",            "logo": "💡"},
  {"name": "Commencis",              "url": "https://www.commencis.com",            "logo": "📱"},
  {"name": "Kafein",                 "url": "https://kafein.com.tr",                "logo": "☕"},
  {"name": "OBSS",                   "url": "https://obss.com.tr",                  "logo": "🔧"},
  {"name": "Invio",                  "url": "https://invio.com.tr",                 "logo": "🚚"},
  {"name": "Opsguru",                "url": "https://opsguru.io",                   "logo": "⚙️"},
  {"name": "Linktera",               "url": "https://linktera.com.tr",              "logo": "🔗"},
  {"name": "Applogist",              "url": "https://applogist.com",                "logo": "📊"},
  {"name": "Teknasyon",              "url": "https://teknasyon.com",                "logo": "🏗️"},
  {"name": "Appcent",                "url": "https://appcent.mobi",                 "logo": "📱"},
  {"name": "Mobven",                 "url": "https://mobven.com",                   "logo": "📲"},
  {"name": "Borusan Teknoloji",      "url": "https://www.borusanteknoloji.com.tr",  "logo": "⚙️"},
  {"name": "NTT Data Turkey",        "url": "https://www.nttdata.com/tr",           "logo": "🔷"},
  {"name": "Capgemini Turkey",       "url": "https://www.capgemini.com/tr-tr",      "logo": "🔵"},
  {"name": "Accenture Turkey",       "url": "https://www.accenture.com/tr-tr",      "logo": "🟣"},
  {"name": "Deloitte Turkey",        "url": "https://www2.deloitte.com/tr",         "logo": "🟢"},
  {"name": "IBM Turkey",             "url": "https://www.ibm.com/tr-tr",            "logo": "🔵"},
  {"name": "SAP Turkey",             "url": "https://www.sap.com/turkey",           "logo": "🔷"},
  {"name": "Oracle Turkey",          "url": "https://www.oracle.com/tr",            "logo": "🔴"},
  {"name": "Ericsson Turkey",        "url": "https://www.ericsson.com/tr",          "logo": "📡"},
  {"name": "Cisco Turkey",           "url": "https://www.cisco.com/c/tr_tr",        "logo": "🔗"},
  {"name": "Wipro Turkey",           "url": "https://www.wipro.com",                "logo": "🌸"},
  {"name": "Globant Turkey",         "url": "https://www.globant.com",              "logo": "🌎"},
  {"name": "EPAM Systems",           "url": "https://www.epam.com",                 "logo": "🔷"},
  {"name": "Teleperformance Turkey", "url": "https://www.teleperformance.com/tr",   "logo": "📞"},
  {"name": "Arvato Systems Turkey",  "url": "https://www.arvato.com/tr",            "logo": "🔷"},

  # ── SAVUNMA & HAVACILIKhttps ────────────────────────────────────────────────
  {"name": "Havelsan",               "url": "https://www.havelsan.com.tr",          "logo": "🛡️"},
  {"name": "Aselsan",                "url": "https://www.aselsan.com.tr",           "logo": "⚡"},
  {"name": "STM Savunma",            "url": "https://www.stm.com.tr",               "logo": "🛡️"},
  {"name": "Baykar Teknoloji",       "url": "https://www.baykartech.com",           "logo": "🛩️"},
  {"name": "Meteksan",               "url": "https://www.meteksan.com",             "logo": "📡"},
  {"name": "Roketsan",               "url": "https://www.roketsan.com.tr",          "logo": "🚀"},
  {"name": "TUSAŞ",                  "url": "https://www.tai.com.tr",               "logo": "✈️"},
  {"name": "Karel",                  "url": "https://www.karel.com.tr",             "logo": "📞"},
  {"name": "Netaş",                  "url": "https://www.netas.com.tr",             "logo": "📡"},

  # ── SEYAHAT & ULAŞIM ────────────────────────────────────────────────────────
  {"name": "Obilet",                 "url": "https://www.obilet.com",               "logo": "🎫"},
  {"name": "Enuygun",                "url": "https://www.enuygun.com",              "logo": "✈️"},
  {"name": "Tatilsepeti",            "url": "https://www.tatilsepeti.com",          "logo": "🏖️"},
  {"name": "Etstur",                 "url": "https://www.etstur.com",               "logo": "✈️"},
  {"name": "Otelz",                  "url": "https://www.otelz.com",               "logo": "🏨"},
  {"name": "Yolcu360",               "url": "https://www.yolcu360.com",             "logo": "🚗"},
  {"name": "Turna.com",              "url": "https://www.turna.com",                "logo": "✈️"},
  {"name": "Tatil.com",              "url": "https://www.tatil.com",                "logo": "🏖️"},
  {"name": "Odamax",                 "url": "https://www.odamax.com",               "logo": "🏨"},
  {"name": "Marti Tech",             "url": "https://marti.tech",                   "logo": "🛴"},
  {"name": "Jolly Tur",              "url": "https://www.jolly.com.tr",             "logo": "🌍"},
  {"name": "Biletall",               "url": "https://www.biletall.com",             "logo": "🎟️"},

  # ── SAĞLIK TEKNOLOJİ ────────────────────────────────────────────────────────
  {"name": "Doktorsitesi",           "url": "https://www.doktorsitesi.com",         "logo": "🏥"},
  {"name": "Doktor Takvimi",         "url": "https://doktortakvimi.com",            "logo": "📅"},
  {"name": "Wellbees",               "url": "https://wellbees.co",                  "logo": "🐝"},
  {"name": "Sağlık Sepeti",          "url": "https://www.sagliksepeti.com",         "logo": "💊"},
  {"name": "Hekimce",                "url": "https://hekimce.com",                  "logo": "🩺"},
  {"name": "Acıbadem",               "url": "https://www.acibadem.com.tr",          "logo": "🏥"},
  {"name": "Memorial Hastanesi",     "url": "https://www.memorial.com.tr",          "logo": "🏥"},

  # ── GAYRİMENKUL TEKNOLOJİ ───────────────────────────────────────────────────
  {"name": "Hepsiemlak",             "url": "https://www.hepsiemlak.com",           "logo": "🏘️"},
  {"name": "Emlakjet",               "url": "https://www.emlakjet.com",             "logo": "✈️"},
  {"name": "Zingat",                 "url": "https://www.zingat.com",               "logo": "🔔"},
  {"name": "Endeksa",                "url": "https://www.endeksa.com",              "logo": "📊"},
  {"name": "Arabam.com",             "url": "https://www.arabam.com",               "logo": "🚗"},
  {"name": "Oto.com.tr",             "url": "https://www.oto.com.tr",               "logo": "🚗"},
  {"name": "Carvak",                 "url": "https://www.carvak.com",               "logo": "🚘"},

  # ── MEDYA & İÇERİK ──────────────────────────────────────────────────────────
  {"name": "Mynet",                  "url": "https://www.mynet.com",                "logo": "🌐"},
  {"name": "Haberler.com",           "url": "https://www.haberler.com",             "logo": "📱"},
  {"name": "BlueTV",                 "url": "https://www.bluetv.com.tr",            "logo": "📺"},
  {"name": "Gain",                   "url": "https://gain.tv",                      "logo": "🎬"},
  {"name": "Puhutv",                 "url": "https://puhutv.com",                   "logo": "🎥"},
  {"name": "beIN Media Turkey",      "url": "https://www.beinsports.com/tr",        "logo": "⚽"},
  {"name": "Digiturk",               "url": "https://www.digiturk.com.tr",          "logo": "📺"},

  # ── LOJİSTİK & TEDARİK ──────────────────────────────────────────────────────
  {"name": "Aras Kargo",             "url": "https://www.araskargo.com.tr",         "logo": "📦"},
  {"name": "Yurtiçi Kargo",          "url": "https://www.yurticicargo.com",         "logo": "🚚"},
  {"name": "MNG Kargo",              "url": "https://www.mngkargo.com.tr",          "logo": "📫"},
  {"name": "Sendeo",                 "url": "https://www.sendeo.com.tr",            "logo": "📨"},

  # ── OTOMOTİV TEKNOLOJİ ──────────────────────────────────────────────────────
  {"name": "Togg",                   "url": "https://www.togg.com.tr",              "logo": "⚡"},
  {"name": "Ford Otosan",            "url": "https://www.fordotosan.com.tr",        "logo": "🚗"},
  {"name": "Tofaş",                  "url": "https://www.tofas.com.tr",             "logo": "🚙"},
  {"name": "Doğuş Otomotiv",         "url": "https://www.dogusotomotiv.com.tr",     "logo": "🚘"},
  {"name": "Otokoç",                 "url": "https://www.otokoc.com.tr",            "logo": "🏢"},

  # ── YAPAY ZEKA & VERİ ───────────────────────────────────────────────────────
  {"name": "Brandnew IO",            "url": "https://www.brandnewio.com",           "logo": "🧠"},
  {"name": "Adjust",                 "url": "https://www.adjust.com",               "logo": "📊"},
  {"name": "Picus Security",         "url": "https://www.picussecurity.com",        "logo": "🔐"},

  # ── İNSAN KAYNAKLARI TEKNOLOJİ ─────────────────────────────────────────────
  {"name": "Kariyer.net",            "url": "https://www.kariyer.net",              "logo": "💼"},
  {"name": "Yenibiris.com",          "url": "https://www.yenibiris.com",            "logo": "👥"},
  {"name": "Workup",                 "url": "https://www.workup.com.tr",            "logo": "💼"},

  # ── EĞİTİM TEKNOLOJİSİ ─────────────────────────────────────────────────────
  {"name": "Tureng",                 "url": "https://tureng.com",                   "logo": "📚"},
  {"name": "Bilge Adam Teknoloji",   "url": "https://www.bilgeadamteknoloji.com",   "logo": "📚"},
  {"name": "Kodlama.io",             "url": "https://www.kodlama.io",               "logo": "💻"},

  # ── ULUSLARARASI FİRMALAR (TR OFİSİ) ───────────────────────────────────────
  {"name": "Microsoft Turkey",       "url": "https://www.microsoft.com/tr-tr",      "logo": "🪟"},
  {"name": "Google Turkey",          "url": "https://careers.google.com",           "logo": "🔍"},
  {"name": "Amazon Turkey",          "url": "https://www.amazon.jobs",              "logo": "📦"},
  {"name": "Salesforce Turkey",      "url": "https://www.salesforce.com/careers",   "logo": "☁️"},
  {"name": "Atlassian",              "url": "https://www.atlassian.com/company/careers","logo":"🅰️"},
  {"name": "Picsart Istanbul",       "url": "https://careers.picsart.com",          "logo": "🎨"},
  {"name": "Jotform",                "url": "https://www.jotform.com/careers",      "logo": "📝"},
  {"name": "Huawei Turkey R&D",      "url": "https://career.huawei.com",            "logo": "📡"},
  {"name": "Siemens Turkey",         "url": "https://new.siemens.com/tr/tr/unternehmen/jobs.html","logo":"⚡"},
  {"name": "Booking.com Istanbul",   "url": "https://jobs.booking.com",             "logo": "🏨"},
  {"name": "Revolut Turkey",         "url": "https://www.revolut.com/careers",      "logo": "🔄"},
  {"name": "Wise Turkey",            "url": "https://www.wise.jobs",                "logo": "💸"},
  {"name": "Klarna Turkey",          "url": "https://www.klarna.com/careers",       "logo": "🛍️"},
  {"name": "Spotify",                "url": "https://www.lifeatspotify.com",        "logo": "🎵"},
  {"name": "TikTok Turkey",          "url": "https://careers.tiktok.com",           "logo": "🎵"},
  {"name": "N26",                    "url": "https://n26.com/en-eu/careers",        "logo": "💳"},
  {"name": "Figma",                  "url": "https://www.figma.com/careers",        "logo": "🎨"},
  {"name": "Notion",                 "url": "https://www.notion.so/careers",        "logo": "📓"},
  {"name": "Stripe",                 "url": "https://stripe.com/jobs",              "logo": "💳"},
  {"name": "Miro",                   "url": "https://miro.com/careers",             "logo": "🖍️"},
  {"name": "Canva",                  "url": "https://www.canva.com/careers",        "logo": "🎨"},
  {"name": "Expedia",                "url": "https://lifeatexpediagroup.com",        "logo": "✈️"},
  {"name": "Trivago Turkey",         "url": "https://www.trivago.com/en-US/selectio/jobs","logo":"🏨"},

  # ── STARTUP & SCALE-UP ──────────────────────────────────────────────────────
  {"name": "Getmobil",               "url": "https://www.getmobil.com",             "logo": "📱"},
  {"name": "Colendi",                "url": "https://colendi.com",                  "logo": "💰"},
  {"name": "Flowla",                 "url": "https://www.flowla.com",               "logo": "🌊"},
  {"name": "Prisync",                "url": "https://prisync.com",                  "logo": "📊"},
]


def main():
    # Mevcut dosyayı yedekle
    backup = FILE.with_suffix(".backup.json")
    with open(FILE) as f:
        old = json.load(f)
    with open(backup, "w", encoding="utf-8") as f:
        json.dump(old, f, ensure_ascii=False, indent=2)
    print(f"📦 Yedek alındı: {backup.name} ({len(old)} firma)")

    # Tekrar edenleri kaldır
    seen_names = set()
    unique = []
    for c in CLEAN_COMPANIES:
        key = c["name"].lower().strip()
        if key not in seen_names:
            seen_names.add(key)
            unique.append(c)

    # Kaydet
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)

    print(f"\n✅ companies.json temizlendi!")
    print(f"   Eski: {len(old)} firma (tahmin URL'li)")
    print(f"   Yeni: {len(unique)} firma (gerçek website URL'li)")
    print(f"\n📋 Format:")
    print(f"   name  → Firma adı")
    print(f"   url   → Gerçek website (smart_scraper kariyer sayfasını otomatik bulacak)")
    print(f"   logo  → Emoji")
    print(f"\n🧠 Kullanım:")
    print(f"   python smart_scraper.py   → Websiteleri ziyaret et, kariyer sayfasını bul, ilanları çek")


if __name__ == "__main__":
    main()
