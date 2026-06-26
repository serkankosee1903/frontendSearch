#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔎 LinkedIn & Kariyer.net'ten Türkiye Yazılım Firmaları
========================================================
Firmaların WEBSİTELERİNİ bulur ve companies.json'a ekler.
Akıllı scraper bu websiteleri ziyaret edip kariyer sayfasını bulacak.
"""

import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin, quote_plus

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()
SCRIPT_DIR = Path(__file__).parent

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def fetch(url: str) -> requests.Response | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=12, allow_redirects=True)
        if r.status_code < 400:
            return r
    except Exception:
        pass
    return None


def clean(text: str) -> str:
    return " ".join(text.strip().split()) if text else ""


# ─── Türk Yazılım Şirketlerinin Gerçek Website URL'leri ──────────────────────
# Bu liste, smart_scraper için seed görevi görür.
# Her firma için name + gerçek website URL'si var.

KNOWN_WEBSITES = [
    # E-ticaret
    {"name": "Trendyol", "url": "https://www.trendyol.com", "logo": "🛒"},
    {"name": "Hepsiburada", "url": "https://www.hepsiburada.com", "logo": "🛍️"},
    {"name": "Getir", "url": "https://getir.com", "logo": "🚀"},
    {"name": "Yemeksepeti", "url": "https://www.yemeksepeti.com", "logo": "🍕"},
    {"name": "Sahibinden", "url": "https://www.sahibinden.com", "logo": "🏠"},
    {"name": "n11", "url": "https://www.n11.com", "logo": "🛒"},
    {"name": "GittiGidiyor", "url": "https://www.gittigidiyor.com", "logo": "🛒"},
    {"name": "Çiçeksepeti", "url": "https://www.ciceksepeti.com", "logo": "🌸"},
    {"name": "Modanisa", "url": "https://www.modanisa.com", "logo": "👗"},
    {"name": "Dolap", "url": "https://dolap.com", "logo": "👕"},
    {"name": "Flo", "url": "https://www.flo.com.tr", "logo": "👟"},
    {"name": "LC Waikiki Digital", "url": "https://www.lcwaikiki.com", "logo": "👕"},
    {"name": "Mavi Jeans", "url": "https://www.mavi.com", "logo": "👖"},
    {"name": "Koton", "url": "https://www.koton.com", "logo": "👗"},
    {"name": "DeFacto", "url": "https://www.defacto.com.tr", "logo": "🧥"},
    {"name": "Boyner", "url": "https://www.boyner.com.tr", "logo": "👔"},
    {"name": "Beymen", "url": "https://www.beymen.com", "logo": "👒"},
    {"name": "Akinon", "url": "https://akinon.com", "logo": "🛍️"},
    {"name": "ikas", "url": "https://ikas.com", "logo": "🛍️"},
    {"name": "Tazedirekt", "url": "https://www.tazedirekt.com", "logo": "🥑"},

    # Fintech
    {"name": "Papara", "url": "https://www.papara.com", "logo": "💳"},
    {"name": "iyzico", "url": "https://www.iyzico.com", "logo": "💰"},
    {"name": "PayTR", "url": "https://www.paytr.com", "logo": "💳"},
    {"name": "Sipay", "url": "https://www.sipay.com.tr", "logo": "💱"},
    {"name": "Param", "url": "https://param.com.tr", "logo": "💰"},
    {"name": "Tosla", "url": "https://tosla.com", "logo": "💸"},
    {"name": "Ininal", "url": "https://www.ininal.com", "logo": "💳"},
    {"name": "Craftgate", "url": "https://craftgate.io", "logo": "💳"},
    {"name": "BtcTurk", "url": "https://www.btcturk.com", "logo": "₿"},
    {"name": "Paribu", "url": "https://www.paribu.com", "logo": "💹"},
    {"name": "Bitexen", "url": "https://bitexen.com", "logo": "₿"},
    {"name": "Icrypex", "url": "https://www.icrypex.com", "logo": "🔐"},
    {"name": "Colendi", "url": "https://colendi.com", "logo": "💰"},
    {"name": "Paycell", "url": "https://paycell.com.tr", "logo": "💳"},
    {"name": "Hopi", "url": "https://hopi.com.tr", "logo": "🎁"},

    # Bankacılık Tech
    {"name": "Garanti BBVA Teknoloji", "url": "https://www.garantibbvateknoloji.com.tr", "logo": "💳"},
    {"name": "Yapı Kredi Teknoloji", "url": "https://www.ykteknoloji.com.tr", "logo": "🏛️"},
    {"name": "İştech", "url": "https://www.istech.com.tr", "logo": "🏦"},
    {"name": "Softtech", "url": "https://www.softtech.com.tr", "logo": "🏦"},
    {"name": "Intertech", "url": "https://www.intertech.com.tr", "logo": "💻"},
    {"name": "Ziraat Teknoloji", "url": "https://www.ziraatteknoloji.com", "logo": "🌾"},
    {"name": "Akbank", "url": "https://www.akbank.com", "logo": "🏦"},
    {"name": "ING Turkey", "url": "https://www.ing.com.tr", "logo": "🏦"},
    {"name": "Fibabanka", "url": "https://www.fibabanka.com.tr", "logo": "🏦"},
    {"name": "Denizbank", "url": "https://www.denizbank.com", "logo": "🏦"},
    {"name": "Sigortam.net", "url": "https://www.sigortam.net", "logo": "🛡️"},
    {"name": "Aksigorta Digital", "url": "https://www.aksigorta.com.tr", "logo": "🛡️"},

    # Telekomünikasyon
    {"name": "Turkcell", "url": "https://www.turkcell.com.tr", "logo": "📱"},
    {"name": "Turkcell Teknoloji", "url": "https://turkcellteknoloji.com.tr", "logo": "📡"},
    {"name": "TT Teknoloji", "url": "https://ttteknoloji.com.tr", "logo": "📞"},
    {"name": "Türk Telekom", "url": "https://www.turktelekom.com.tr", "logo": "📶"},
    {"name": "Vodafone Turkey", "url": "https://www.vodafone.com.tr", "logo": "📶"},
    {"name": "Superonline", "url": "https://www.superonline.net", "logo": "🌐"},
    {"name": "TurkNet", "url": "https://www.turknet.net.tr", "logo": "🌐"},
    {"name": "BiP", "url": "https://bip.com.tr", "logo": "💬"},
    {"name": "Paycell", "url": "https://paycell.com.tr", "logo": "💳"},

    # Oyun
    {"name": "Dream Games", "url": "https://www.dreamgames.com", "logo": "🎯"},
    {"name": "Peak Games", "url": "https://www.peakgames.net", "logo": "🎮"},
    {"name": "Spyke Games", "url": "https://www.spykegames.com", "logo": "🎮"},
    {"name": "Rollic Games", "url": "https://rollic.games", "logo": "🎲"},
    {"name": "Gram Games", "url": "https://www.gramgames.com", "logo": "🎯"},
    {"name": "Masomo", "url": "https://masomo.com", "logo": "⚽"},
    {"name": "Bigger Games", "url": "https://www.biggergames.com", "logo": "🎮"},
    {"name": "Codeway", "url": "https://codeway.co", "logo": "📱"},
    {"name": "Good Job Games", "url": "https://goodjobgames.com", "logo": "✅"},
    {"name": "Fugo Games", "url": "https://fugogames.com", "logo": "🎮"},
    {"name": "Joygame", "url": "https://www.joygame.com", "logo": "😄"},

    # SaaS & Kurumsal
    {"name": "Logo Yazılım", "url": "https://www.logo.com.tr", "logo": "💼"},
    {"name": "Insider", "url": "https://useinsider.com", "logo": "📊"},
    {"name": "Segmentify", "url": "https://www.segmentify.com", "logo": "📈"},
    {"name": "UserGuiding", "url": "https://userguiding.com", "logo": "👥"},
    {"name": "Prisync", "url": "https://prisync.com", "logo": "📊"},
    {"name": "Storyly", "url": "https://storyly.io", "logo": "📖"},
    {"name": "Jotform", "url": "https://www.jotform.com", "logo": "📝"},
    {"name": "Appsention", "url": "https://appsention.com", "logo": "📱"},
    {"name": "Testinium", "url": "https://testinium.com", "logo": "🧪"},
    {"name": "Appcircle", "url": "https://appcircle.io", "logo": "⭕"},
    {"name": "Vispera", "url": "https://vispera.co", "logo": "👁️"},
    {"name": "Bimser", "url": "https://www.bimser.com.tr", "logo": "⚙️"},
    {"name": "IdeaSoft", "url": "https://www.ideasoft.com.tr", "logo": "💡"},
    {"name": "Paraşüt", "url": "https://parasut.com", "logo": "📋"},
    {"name": "Netmera", "url": "https://netmera.com", "logo": "📱"},
    {"name": "NetGSM", "url": "https://www.netgsm.com.tr", "logo": "📱"},
    {"name": "Picus Security", "url": "https://www.picussecurity.com", "logo": "🔐"},
    {"name": "Berqnet", "url": "https://www.berqnet.com", "logo": "🔒"},
    {"name": "Logsign", "url": "https://www.logsign.com", "logo": "📊"},
    {"name": "Keepnet Labs", "url": "https://keepnetlabs.com", "logo": "🔐"},
    {"name": "Prodaft", "url": "https://www.prodaft.com", "logo": "🕵️"},

    # IT Hizmetleri
    {"name": "KoçSistem", "url": "https://www.kocsistem.com.tr", "logo": "🏢"},
    {"name": "Doğuş Teknoloji", "url": "https://www.dogussteknoloji.com", "logo": "🏢"},
    {"name": "Borusan Teknoloji", "url": "https://www.borusanteknoloji.com.tr", "logo": "⚙️"},
    {"name": "Etiya", "url": "https://www.etiya.com", "logo": "🔷"},
    {"name": "Innova", "url": "https://www.innova.com.tr", "logo": "💡"},
    {"name": "Commencis", "url": "https://www.commencis.com", "logo": "📱"},
    {"name": "Kafein", "url": "https://kafein.com.tr", "logo": "☕"},
    {"name": "OBSS", "url": "https://obss.com.tr", "logo": "🔧"},
    {"name": "Invio", "url": "https://invio.com.tr", "logo": "🚚"},
    {"name": "Opsguru", "url": "https://opsguru.io", "logo": "⚙️"},
    {"name": "Linktera", "url": "https://linktera.com.tr", "logo": "🔗"},
    {"name": "Applogist", "url": "https://applogist.com", "logo": "📊"},
    {"name": "Teknasyon", "url": "https://teknasyon.com", "logo": "🏗️"},
    {"name": "Appcent", "url": "https://appcent.mobi", "logo": "📱"},
    {"name": "Mobven", "url": "https://mobven.com", "logo": "📲"},

    # Seyahat
    {"name": "Obilet", "url": "https://www.obilet.com", "logo": "🎫"},
    {"name": "Enuygun", "url": "https://www.enuygun.com", "logo": "✈️"},
    {"name": "Tatilsepeti", "url": "https://www.tatilsepeti.com", "logo": "🏖️"},
    {"name": "Etstur", "url": "https://www.etstur.com", "logo": "✈️"},
    {"name": "Otelz", "url": "https://www.otelz.com", "logo": "🏨"},
    {"name": "Yolcu360", "url": "https://www.yolcu360.com", "logo": "🚗"},
    {"name": "Turna.com", "url": "https://www.turna.com", "logo": "✈️"},
    {"name": "Marti Tech", "url": "https://marti.tech", "logo": "🛴"},

    # Gayrimenkul
    {"name": "Hepsiemlak", "url": "https://www.hepsiemlak.com", "logo": "🏘️"},
    {"name": "Emlakjet", "url": "https://www.emlakjet.com", "logo": "✈️"},
    {"name": "Zingat", "url": "https://www.zingat.com", "logo": "🔔"},
    {"name": "Endeksa", "url": "https://www.endeksa.com", "logo": "📊"},
    {"name": "Apsiyon", "url": "https://apsiyon.com", "logo": "🏠"},

    # Otomotiv
    {"name": "Arabam.com", "url": "https://www.arabam.com", "logo": "🚗"},
    {"name": "Oto.com.tr", "url": "https://www.oto.com.tr", "logo": "🚗"},
    {"name": "Togg", "url": "https://www.togg.com.tr", "logo": "⚡"},
    {"name": "Ford Otosan", "url": "https://www.fordotosan.com.tr", "logo": "🚗"},

    # Savunma
    {"name": "Havelsan", "url": "https://www.havelsan.com.tr", "logo": "🛡️"},
    {"name": "Aselsan", "url": "https://www.aselsan.com.tr", "logo": "⚡"},
    {"name": "STM Savunma", "url": "https://www.stm.com.tr", "logo": "🛡️"},
    {"name": "Baykar Teknoloji", "url": "https://www.baykartech.com", "logo": "🛩️"},
    {"name": "Meteksan", "url": "https://www.meteksan.com", "logo": "📡"},

    # Sağlık Tech
    {"name": "Doktorsitesi", "url": "https://www.doktorsitesi.com", "logo": "🏥"},
    {"name": "Doktor Takvimi", "url": "https://doktortakvimi.com", "logo": "📅"},
    {"name": "Wellbees", "url": "https://wellbees.co", "logo": "🐝"},

    # Medya
    {"name": "Mynet", "url": "https://www.mynet.com", "logo": "🌐"},
    {"name": "Haberler.com", "url": "https://www.haberler.com", "logo": "📱"},
    {"name": "BlueTV", "url": "https://www.bluetv.com.tr", "logo": "📺"},
    {"name": "Gain", "url": "https://gain.tv", "logo": "🎬"},
    {"name": "Puhutv", "url": "https://puhutv.com", "logo": "🎥"},

    # Lojistik
    {"name": "Aras Kargo", "url": "https://www.araskargo.com.tr", "logo": "📦"},
    {"name": "Yurtiçi Kargo", "url": "https://www.yurticikargo.com", "logo": "🚚"},
    {"name": "MNG Kargo", "url": "https://www.mngkargo.com.tr", "logo": "📫"},
    {"name": "Sendeo", "url": "https://www.sendeo.com.tr", "logo": "📨"},

    # AI/Startup
    {"name": "Brandnew IO", "url": "https://www.brandnewio.com", "logo": "🧠"},
    {"name": "Vispera", "url": "https://vispera.co", "logo": "👁️"},
    {"name": "Picus Security", "url": "https://www.picussecurity.com", "logo": "🔐"},
    {"name": "Adjust", "url": "https://www.adjust.com", "logo": "📊"},
]


def get_linkedin_companies() -> list[dict]:
    """LinkedIn Turkey'den yazılım şirketi isimlerini + websitelerini çeker."""
    companies = []
    queries = [
        "software+company+turkey",
        "teknoloji+firma+istanbul",
        "yazilim+sirketi+turkey",
    ]

    for query in queries:
        url = (
            f"https://www.linkedin.com/search/results/companies/?"
            f"keywords={query}&geoUrn=urn%3Ali%3Ageo%3A102256854"  # Turkey
        )
        resp = fetch(url)
        if not resp:
            time.sleep(1)
            continue

        soup = BeautifulSoup(resp.text, "lxml")

        # Şirket kartları
        for card in soup.select(
            ".entity-result__item, .search-result__wrapper, "
            "[data-control-name='search_srp_result']"
        ):
            name_el = card.select_one(
                ".entity-result__title-text, .search-result__title, "
                ".actor-name, span[aria-hidden='true']"
            )
            website_el = card.select_one(
                "[data-tracking-control-name*='website'], "
                "a[href*='linkedin.com/company']"
            )

            name = clean(name_el.get_text()) if name_el else ""
            if not name or len(name) < 2:
                continue

            companies.append({
                "name": name,
                "url": "",
                "logo": "💼",
                "source": "linkedin_discovery",
            })

        time.sleep(1.5)

    return companies


def get_kariyer_net_companies() -> list[dict]:
    """
    Kariyer.net firma dizininden Bilişim/Teknoloji sektöründeki
    firmaların adını ve websitesini çeker.
    """
    companies = []
    seen = set()

    # Teknoloji sektörü sayfaları
    sector_urls = [
        "https://www.kariyer.net/firmalar?sektor=Bilisim+Teknolojileri",
        "https://www.kariyer.net/firmalar?sektor=Yazilim",
        "https://www.kariyer.net/firmalar?sektor=Internet",
        "https://www.kariyer.net/firmalar?sektor=Eticaret",
        "https://www.kariyer.net/firmalar?sektor=Telekomunikasyon",
        "https://www.kariyer.net/firmalar?sektor=Oyun",
    ]

    for sector_url in sector_urls:
        for page in range(1, 15):
            url = f"{sector_url}&page={page}" if page > 1 else sector_url
            resp = fetch(url)
            if not resp:
                break

            soup = BeautifulSoup(resp.text, "lxml")

            # Firma linkleri
            firm_links = soup.select("a[href*='/firma/']")
            if not firm_links:
                break

            page_new = 0
            for a in firm_links:
                name = clean(a.get_text())
                href = a.get("href", "")

                if not name or len(name) < 2 or name.lower() in seen:
                    continue
                seen.add(name.lower())

                # Firma detay sayfasından website çekmeyi deneyebiliriz
                # Şimdilik sadece isim + kariyer.net profil URL'sini kaydet
                kn_profile = (
                    urljoin("https://www.kariyer.net", href)
                    if href else ""
                )

                companies.append({
                    "name": name,
                    "url": "",  # Website sonra bulunacak
                    "kariyer_net_profile": kn_profile,
                    "logo": "🌐",
                    "source": "kariyer_net_discovery",
                })
                page_new += 1

            if page_new == 0:
                break
            time.sleep(0.8)

    return companies


def enrich_with_website(company: dict) -> dict:
    """
    Firma adından Google benzeri arama ile website URL'sini bulmaya çalışır.
    (DuckDuckGo arama kullanır - auth gerektirmez)
    """
    if company.get("url"):
        return company  # Zaten var

    name = company["name"]
    search_url = f"https://duckduckgo.com/html/?q={quote_plus(name + ' resmi site türkiye')}"

    resp = fetch(search_url)
    if not resp:
        return company

    soup = BeautifulSoup(resp.text, "lxml")
    results = soup.select(".result__url, .result__title a, a.result__a")

    for r in results[:3]:
        href = r.get("href", "") or r.get_text()
        # Şirkete ait ana domain bul
        if not href.startswith("http"):
            continue

        parsed_href = urlparse(href)
        domain = parsed_href.netloc.lower()

        # Sosyal medya ve bilinen platformları atla
        skip = ["linkedin", "twitter", "facebook", "instagram",
                "wikipedia", "kariyer.net", "indeed", "glassdoor",
                "youtube", "google", "bing"]
        if any(s in domain for s in skip):
            continue

        company["url"] = f"{parsed_href.scheme}://{domain}"
        break

    return company


def update_companies_json(new_companies: list[dict]) -> int:
    """Mevcut companies.json'a yeni firmaları ekler, websitesi olanları önceliklendirir."""
    companies_file = SCRIPT_DIR / "companies.json"

    with open(companies_file, "r", encoding="utf-8") as f:
        existing = json.load(f)

    # Mevcut firmaların adlarını topla
    existing_names = {c["name"].lower().strip() for c in existing}

    # Mevcut firmaların URL'lerini güncelle (boşsa)
    existing_by_name = {c["name"].lower().strip(): i for i, c in enumerate(existing)}

    added = 0
    updated = 0

    for company in new_companies:
        name = company.get("name", "").lower().strip()
        if not name:
            continue

        if name in existing_by_name:
            # Mevcut firmayı güncelle (URL boşsa doldur)
            idx = existing_by_name[name]
            if not existing[idx].get("url") and company.get("url"):
                existing[idx]["url"] = company["url"]
                updated += 1
        else:
            # Yeni firma ekle
            company.setdefault("career_url", "")
            company.setdefault("type", "smart")  # smart_scraper kullanacak
            existing.append(company)
            existing_names.add(name)
            existing_by_name[name] = len(existing) - 1
            added += 1

    with open(companies_file, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    return added, updated


def run_discovery():
    """Tüm kaynaklardan firma keşfi + website zenginleştirme."""
    console.print("\n[bold cyan]🔎 Türkiye Yazılım Firmaları Keşif ve Zenginleştirme[/bold cyan]\n")

    all_new = []

    # 1. Bilinen website listesini ekle
    console.log("  📋 Bilinen firma websiteleri yükleniyor...")
    added, updated = update_companies_json(KNOWN_WEBSITES)
    console.log(f"  ✅ Bilinen websiteler: {added} yeni, {updated} güncellendi")

    # 2. Kariyer.net firma dizini
    console.log("  🌐 Kariyer.net firma dizini taranıyor...")
    kn_companies = get_kariyer_net_companies()
    console.log(f"  Kariyer.net: {len(kn_companies)} firma bulundu")
    all_new.extend(kn_companies)

    # 3. LinkedIn (public)
    console.log("  💼 LinkedIn Turkey şirketi taranıyor...")
    li_companies = get_linkedin_companies()
    console.log(f"  LinkedIn: {len(li_companies)} firma")
    all_new.extend(li_companies)

    # 4. Yeni firmaları ekle
    if all_new:
        added2, updated2 = update_companies_json(all_new)
        console.log(f"  ✅ Keşif sonuçları: {added2} yeni firma")

    # 5. Sonuç
    companies_file = SCRIPT_DIR / "companies.json"
    with open(companies_file) as f:
        final = json.load(f)

    has_url = sum(1 for c in final if c.get("url"))
    console.print(f"\n[bold green]✅ Güncellendi![/bold green]")
    console.print(f"  📊 Toplam firma: {len(final)}")
    console.print(f"  🌐 Website URL'si olan: {has_url}")
    console.print(f"  🔍 Akıllı scraper bu websiteleri ziyaret edecek\n")


if __name__ == "__main__":
    run_discovery()
