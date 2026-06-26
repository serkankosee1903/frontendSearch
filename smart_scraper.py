#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 Akıllı Kariyer Sayfası Keşif Motoru
========================================
Firma websitesine gidip kariyer sayfasını otomatik bulur,
hangi ATS kullandığını tespit eder ve ilanları çeker.

Desteklenen ATS Platformları:
  - Teamtailor   (teamtailor.com)
  - Lever        (jobs.lever.co)
  - Greenhouse   (boards.greenhouse.io)
  - Workday      (myworkdayjobs.com)
  - Breezy HR    (breezy.hr)
  - SmartRecruiters
  - Recruitee
  - Personio
  - BambooHR
  - İkas (yerel)
  - Kariyer.net  (fallback)
"""

import json
import re
import time
import hashlib
from pathlib import Path
from urllib.parse import urljoin, urlparse, quote_plus
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()
SCRIPT_DIR = Path(__file__).parent

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
TIMEOUT = 12


# ─── Filtre Kelimeleri ────────────────────────────────────────────────────────

SENIOR_FE_PATTERNS = [
    r"senior\s+front[\s\-]?end",
    r"kıdemli\s+front[\s\-]?end",
    r"sr\.?\s*front[\s\-]?end",
    r"lead\s+front[\s\-]?end",
    r"principal\s+front[\s\-]?end",
    r"senior\s+frontend",
    r"kıdemli\s+frontend",
    r"senior\s+ui\s+(developer|engineer|dev)",
    r"senior\s+react(\.?js)?\s*(developer|engineer|dev)?",
    r"senior\s+vue(\.?js)?\s*(developer|engineer|dev)?",
    r"senior\s+angular\s*(developer|engineer|dev)?",
    r"senior\s+javascript\s*(developer|engineer|dev)?",
    r"senior\s+typescript\s*(developer|engineer|dev)?",
    r"senior\s+web\s+(developer|engineer|dev)",
    r"lead\s+ui\s*(developer|engineer)?",
    r"staff\s+front[\s\-]?end",
    r"kıdemli\s+react",
    r"senior\s+next\.?js",
    r"senior\s+nuxt\.?js",
    r"frontend\s+lead",
    r"front.end\s+lead",
]

FRONTEND_KW = [
    "frontend", "front-end", "front end",
    "react", "reactjs", "vue", "vuejs", "angular",
    "nextjs", "next.js", "nuxtjs", "nuxt.js",
    "javascript", "typescript",
    "ui developer", "ui engineer",
    "web developer", "web engineer",
    "web geliştirici",
]

SENIOR_IND = [
    "senior", "sr.", "sr ", "kıdemli", "lead",
    "principal", "staff", "head of",
]

EXCLUDE_RE = [
    r"junior", r"jr\.", r"\bintern\b", r"stajyer", r"entry.level",
    r"\bbackend\b", r"\bback.end\b", r"\bback end\b",
    r"\bdevops\b", r"\bmobile\s+developer\b", r"\bandroid\b", r"\bios\s+dev",
    r"\bdata\s+scientist\b", r"\bmachine\s+learning\b",
    r"\bqa\s+engineer\b", r"\btest\s+engineer\b",
    r"\bproduct\s+manager\b", r"\bscrum\s+master\b",
    r"\bgraphic\s+designer\b",
]


def is_senior_fe(title: str) -> bool:
    t = title.lower().strip()
    if any(re.search(p, t) for p in EXCLUDE_RE):
        return False
    # Frontend kelimesi geçmesi yeterli (Senior olma şartı kaldırıldı)
    has_fe = any(kw in t for kw in FRONTEND_KW)
    return has_fe or any(re.search(p, t) for p in SENIOR_FE_PATTERNS)


def clean(text: str) -> str:
    return " ".join(text.strip().split()) if text else ""


def uid(company: str, title: str) -> str:
    return hashlib.md5(f"{company}:{title}".lower().encode()).hexdigest()[:8]


def make_job(company, logo, title, url, location="Türkiye", dept="Engineering", source="web"):
    return {
        "id": uid(company, title),
        "company": company,
        "logo": logo,
        "title": clean(title),
        "url": url,
        "location": location or "Türkiye",
        "department": dept,
        "tags": [],
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
    }


def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response | None:
    """HTTP isteği yapar."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout,
                         allow_redirects=True)
        if r.status_code < 400:
            return r
        return None
    except requests.exceptions.SSLError:
        try:
            r = requests.get(url, headers=HEADERS, timeout=timeout,
                             allow_redirects=True, verify=False)
            if r.status_code < 400:
                return r
        except Exception:
            pass
        return None
    except Exception:
        return None


# ════════════════════════════════════════════════════════════════════════════════
# ATS Platform Tespiti
# ════════════════════════════════════════════════════════════════════════════════

# URL veya sayfa içeriğinden ATS platformunu tespit etmek için
ATS_SIGNATURES = {
    # URL tabanlı
    "teamtailor.com":       "teamtailor",
    "jobs.lever.co":        "lever",
    "lever.co/":            "lever",
    "boards.greenhouse.io": "greenhouse",
    "greenhouse.io":        "greenhouse",
    "myworkdayjobs.com":    "workday",
    "breezy.hr":            "breezy",
    "smartrecruiters.com":  "smartrecruiters",
    "app.recruitee.com":    "recruitee",
    "recruitee.com":        "recruitee",
    "personio.com":         "personio",
    "join.com":             "join",
    "bamboohr.com":         "bamboohr",
    "comeet.co":            "comeet",
    "taleo.net":            "taleo",
    "successfactors.com":   "successfactors",
    "icims.com":            "icims",
    "workable.com":         "workable",
    "ashbyhq.com":          "ashby",
    "notion.so":            "notion",
}

# Sayfa içeriğinden ATS tespiti
ATS_CONTENT_SIGNATURES = {
    "teamtailor":      ["teamtailor", "tt-job-listing", "tt-careers"],
    "lever":           ["jobs.lever.co", "lever-jobs", "postings"],
    "greenhouse":      ["greenhouse.io", "gh-board"],
    "workday":         ["workday", "myworkdayjobs"],
    "breezy":          ["breezy.hr", "breezy-jobs"],
    "smartrecruiters": ["smartrecruiters", "sr-jobs"],
    "workable":        ["workable.com", "jobs.workable"],
    "ashby":           ["ashbyhq.com", "ashby-job"],
}


def detect_ats_from_url(url: str) -> str | None:
    """URL'den ATS platform adını tespit eder."""
    url_lower = url.lower()
    for sig, platform in ATS_SIGNATURES.items():
        if sig in url_lower:
            return platform
    return None


def detect_ats_from_content(html: str) -> str | None:
    """Sayfa içeriğinden ATS platform adını tespit eder."""
    html_lower = html.lower()
    for platform, sigs in ATS_CONTENT_SIGNATURES.items():
        if any(s in html_lower for s in sigs):
            return platform
    return None


# ════════════════════════════════════════════════════════════════════════════════
# Kariyer Sayfası Keşfi
# ════════════════════════════════════════════════════════════════════════════════

# Denenecek yol desenleri
CAREER_PATHS = [
    "/kariyer", "/kariyer/ilan", "/kariyer/is-ilanlari",
    "/careers", "/careers/open-positions", "/careers/jobs",
    "/jobs", "/open-positions", "/acik-pozisyonlar",
    "/tr/kariyer", "/en/careers", "/en/jobs",
    "/join-us", "/join", "/work-with-us",
    "/about/careers", "/about/jobs",
    "/company/careers", "/company/jobs",
    "/team", "/our-team/join",
    "/is-ilanlari", "/pozisyonlar",
]

# Kariyer sayfası link kelime kalıpları (sayfadaki <a> metinleri)
CAREER_LINK_KEYWORDS = [
    "kariyer", "career", "careers", "jobs", "is-ilan", "iş ilan",
    "pozisyon", "apply", "join us", "join our", "work with us",
    "açık pozisyon", "bize katıl", "ekibimize katıl",
    "iş başvuru", "is basvur",
]


def find_career_page(base_url: str) -> str | None:
    """
    Firma websitesinde kariyer sayfasını bulur.

    Strateji:
    1. Ana sayfadaki linklere bak → kariyer/jobs linkleri
    2. ATS platformunu tespit edince o sayfaya gidip ATS linkini takip et
    3. Yaygın kariyer URL yollarını dene
    """
    parsed = urlparse(base_url)
    root = f"{parsed.scheme}://{parsed.netloc}"

    def _extract_ats_or_career_link(soup, page_url):
        """Sayfadan ATS veya kariyer linki çıkarır."""
        for a in soup.find_all("a", href=True):
            href = a.get("href", "").strip()
            text = a.get_text(strip=True).lower()
            if not href:
                continue

            full = href if href.startswith("http") else (
                root + href if href.startswith("/") else urljoin(page_url, href)
            )

            # Doğrudan ATS URL'si mi?
            if detect_ats_from_url(full):
                return full

            # Kariyer kelimesi içeriyor mu?
            is_career_text = any(kw in text for kw in CAREER_LINK_KEYWORDS)
            is_career_href = any(kw in href.lower() for kw in [
                "kariyer", "career", "/jobs", "pozisyon", "is-ilan",
                "join", "vacancy", "vacancies", "apply", "hiring"
            ])
            if is_career_text or is_career_href:
                if any(kw in full.lower() for kw in [
                    "kariyer", "career", "jobs", "pozisyon", "ilan", "vacancy"
                ]):
                    return full

        # iframe içindeki ATS
        for iframe in soup.find_all("iframe", src=True):
            src = iframe["src"]
            full = src if src.startswith("http") else urljoin(page_url, src)
            if detect_ats_from_url(full):
                return full
        return None

    # ── 1. Ana sayfayı çek ────────────────────────────────────────────────────
    resp = fetch(base_url)
    if resp:
        soup = BeautifulSoup(resp.text, "lxml")
        link = _extract_ats_or_career_link(soup, base_url)
        if link:
            # Eğer bu bir ara kariyer sayfasıysa (kendi domaini),
            # bir kez daha git ve içinde ATS linki var mı bak
            if not detect_ats_from_url(link) and urlparse(link).netloc == parsed.netloc:
                resp2 = fetch(link, timeout=8)
                if resp2:
                    soup2 = BeautifulSoup(resp2.text, "lxml")
                    ats_link = _extract_ats_or_career_link(soup2, link)
                    if ats_link:
                        return ats_link
                    # Sayfada anlamlı ilan içeriği var mı?
                    if any(kw in resp2.text.lower() for kw in
                           ["senior", "developer", "engineer", "apply"]):
                        return link
            return link

        # Sayfa içeriğinde ATS imzası var mı ama link yoksa
        ats = detect_ats_from_content(resp.text)
        if ats:
            link = _extract_ats_or_career_link(soup, base_url)
            if link:
                return link

    # ── 2. Yaygın kariyer URL yollarını dene ──────────────────────────────────
    for path in CAREER_PATHS:
        candidate = root + path
        r = fetch(candidate, timeout=8)
        if r and len(r.text) > 2000:
            soup = BeautifulSoup(r.text, "lxml")
            # Bu sayfada ATS linki var mı?
            ats_link = _extract_ats_or_career_link(soup, candidate)
            if ats_link:
                return ats_link
            body_text = soup.get_text(strip=True).lower()
            if any(kw in body_text for kw in [
                "senior", "developer", "engineer", "pozisyon",
                "kariyer", "jobs", "vacancy", "apply", "açık"
            ]):
                return candidate

    return None


# ════════════════════════════════════════════════════════════════════════════════
# Platform-Spesifik Scraper'lar
# ════════════════════════════════════════════════════════════════════════════════

def scrape_teamtailor(career_url: str, company: str, logo: str) -> list[dict]:
    """Teamtailor sayfasından ilanları çeker."""
    jobs = []
    parsed = urlparse(career_url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    resp = fetch(career_url)
    if not resp:
        return jobs

    soup = BeautifulSoup(resp.text, "lxml")

    # Teamtailor link yapısı: /jobs/XXXX-pozisyon-adi
    for a in soup.find_all("a", href=True):
        href = a["href"]
        title = clean(a.get_text())
        if not title or len(title) < 4:
            continue
        if "/jobs/" in href and is_senior_fe(title):
            full = href if href.startswith("http") else urljoin(base, href)
            jobs.append(make_job(company, logo, title, full, source="teamtailor"))

    return jobs


def scrape_lever(career_url: str, company: str, logo: str) -> list[dict]:
    """Lever sayfasından ilanları çeker (.posting yapısı)."""
    jobs = []
    resp = fetch(career_url)
    if not resp:
        return jobs

    soup = BeautifulSoup(resp.text, "lxml")
    postings = soup.select(".posting")

    for posting in postings:
        title_el = posting.select_one(".posting-title h5, h5.posting-title, .posting-title")
        link_el = posting.select_one("a[href*='/jobs/']") or posting.find("a", href=True)
        loc_el = posting.select_one(".sort-by-location, .posting-categories .sort-by-location")

        title = clean(title_el.get_text()) if title_el else ""
        if not title and link_el:
            title = clean(link_el.get_text())
        location = clean(loc_el.get_text()) if loc_el else "Türkiye"
        href = link_el["href"] if link_el else career_url
        if href and not href.startswith("http"):
            href = urljoin(career_url, href)

        if title and is_senior_fe(title):
            jobs.append(make_job(company, logo, title, href, location=location, source="lever"))

    # Lever iframe içinde olabilir
    if not postings:
        for a in soup.find_all("a", href=True):
            title = clean(a.get_text())
            if title and len(title) > 4 and is_senior_fe(title):
                href = a["href"]
                if not href.startswith("http"):
                    href = urljoin(career_url, href)
                jobs.append(make_job(company, logo, title, href, source="lever"))

    return jobs


def scrape_greenhouse(career_url: str, company: str, logo: str) -> list[dict]:
    """Greenhouse boards sayfasından ilanları çeker."""
    jobs = []
    # Greenhouse JSON API: boards.greenhouse.io/COMPANY/jobs
    parsed = urlparse(career_url)
    slug = parsed.path.split("/")[1] if parsed.path else ""

    if slug:
        api_url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
        resp = fetch(api_url)
        if resp:
            try:
                data = resp.json()
                for job in data.get("jobs", []):
                    title = job.get("title", "")
                    if title and is_senior_fe(title):
                        location = job.get("location", {}).get("name", "Türkiye")
                        jobs.append(make_job(
                            company, logo, title,
                            job.get("absolute_url", career_url),
                            location=location, source="greenhouse"
                        ))
                return jobs
            except Exception:
                pass

    # HTML fallback
    resp = fetch(career_url)
    if not resp:
        return jobs
    soup = BeautifulSoup(resp.text, "lxml")
    for a in soup.select(".opening a, .job-post a, a.job-title"):
        title = clean(a.get_text())
        if title and is_senior_fe(title):
            href = a["href"]
            if not href.startswith("http"):
                href = urljoin(career_url, href)
            jobs.append(make_job(company, logo, title, href, source="greenhouse"))

    return jobs


def scrape_workable(career_url: str, company: str, logo: str) -> list[dict]:
    """Workable sayfasından ilanları çeker."""
    jobs = []
    resp = fetch(career_url)
    if not resp:
        return jobs

    soup = BeautifulSoup(resp.text, "lxml")

    # Workable: li[data-ui="job"] yapısı
    for item in soup.select("li[data-ui='job'], .jobs-list-item, [class*='job-item']"):
        a = item.find("a", href=True)
        title_el = item.select_one("h2, h3, .job-title, [class*='title']")
        title = clean(title_el.get_text()) if title_el else (clean(a.get_text()) if a else "")
        if not title or not a:
            continue
        if is_senior_fe(title):
            href = a["href"]
            if not href.startswith("http"):
                href = urljoin(career_url, href)
            jobs.append(make_job(company, logo, title, href, source="workable"))

    return jobs


def scrape_generic(career_url: str, company: str, logo: str,
                   source: str = "web") -> list[dict]:
    """Bilinmeyen bir kariyer sayfasını genel yöntemle tarar."""
    jobs = []
    resp = fetch(career_url)
    if not resp:
        return jobs

    soup = BeautifulSoup(resp.text, "lxml")

    # İş başlığı içeren tüm linkleri bul
    job_selectors = [
        "a[href*='/job'], a[href*='/jobs'], a[href*='/kariyer']",
        "a[href*='/position'], a[href*='/vacancy'], a[href*='/apply']",
        ".job-title a, .position-title a, .opening-title a",
        "h2 a, h3 a, h4 a",
        "li[class*='job'] a, li[class*='position'] a",
        "[class*='job-title'], [class*='position-name']",
    ]

    seen = set()
    for sel in job_selectors:
        for elem in soup.select(sel):
            title = clean(elem.get_text())
            if not title or len(title) < 4 or title in seen:
                continue
            seen.add(title)

            if is_senior_fe(title):
                href = elem.get("href", career_url)
                if href and not href.startswith("http"):
                    href = urljoin(career_url, href)
                jobs.append(make_job(company, logo, title,
                                     href or career_url, source=source))

    return jobs


def scrape_kariyer_net_fallback(company_name: str, logo: str) -> list[dict]:
    """
    Kariyer sayfası bulunamayan firmalar için
    Kariyer.net'te arama yapar.
    """
    jobs = []
    url = f"https://www.kariyer.net/is-ilani?firma={quote_plus(company_name)}"
    resp = fetch(url)
    if not resp:
        return jobs

    soup = BeautifulSoup(resp.text, "lxml")
    for a in soup.select("a[href*='/is-ilani/']"):
        title = clean(a.get_text())
        if not title or len(title) < 4:
            continue
        if is_senior_fe(title):
            href = a["href"]
            if not href.startswith("http"):
                href = f"https://www.kariyer.net{href}"
            jobs.append(make_job(
                company_name, logo, title, href,
                source=f"kariyer.net"
            ))

    return jobs


# ════════════════════════════════════════════════════════════════════════════════
# Ana Akıllı Scraper
# ════════════════════════════════════════════════════════════════════════════════

def smart_scrape_company(company: dict) -> tuple[list[dict], str]:
    """
    Bir firmayı akıllıca tarar:
    1. Web sitesinde kariyer sayfasını bul
    2. ATS platformunu tespit et
    3. Uygun scraper ile ilanları çek
    
    Returns: (jobs, status_message)
    """
    name = company["name"]
    logo = company.get("logo", "🏢")
    website = company.get("url", "")
    given_career_url = company.get("career_url", "")

    # ── Adım 1: Kariyer URL'sini belirle ──────────────────────────────────────

    career_url = None

    # Eğer verilen career_url zaten bilinen bir ATS platfomuysa direkt kullan
    if given_career_url and detect_ats_from_url(given_career_url):
        career_url = given_career_url
    # Eğer verilen career_url gerçekçiyse önce onu dene
    elif given_career_url and given_career_url.startswith("http"):
        resp = fetch(given_career_url, timeout=8)
        if resp and len(resp.text) > 1000:
            career_url = given_career_url
            # ATS tespiti yap
            ats_from_content = detect_ats_from_content(resp.text)
            if ats_from_content:
                # İçerikte ATS link var mı?
                soup = BeautifulSoup(resp.text, "lxml")
                for a in soup.find_all("a", href=True):
                    if detect_ats_from_url(a["href"]):
                        career_url = a["href"] if a["href"].startswith("http") else urljoin(given_career_url, a["href"])
                        break

    # Websiteden otomatik keşfet
    if not career_url and website and website.startswith("http"):
        career_url = find_career_page(website)

    # Websiteyi career_url olarak dene
    if not career_url and given_career_url:
        career_url = given_career_url

    # ── Adım 2: ATS'yi tespit et ve scrape et ─────────────────────────────────

    def _find_ats_url_in_page(page_url: str) -> tuple[str | None, str | None]:
        """
        Bir sayfa URL'sine gidip içindeki gerçek ATS URL'sini bulur.
        Returns: (ats_url, ats_platform)
        """
        resp = fetch(page_url)
        if not resp:
            return None, None
        soup = BeautifulSoup(resp.text, "lxml")

        # Önce linklerde ATS URL ara
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if not href.startswith("http"):
                href = urljoin(page_url, href)
            platform = detect_ats_from_url(href)
            if platform:
                return href, platform

        # iframe'lerde ara
        for iframe in soup.find_all("iframe", src=True):
            src = iframe["src"]
            if not src.startswith("http"):
                src = urljoin(page_url, src)
            platform = detect_ats_from_url(src)
            if platform:
                return src, platform

        # İçerik imzasından ATS tespit et
        ats_platform = detect_ats_from_content(resp.text)
        if ats_platform:
            return page_url, ats_platform

        return None, None

    if career_url:
        # URL'den direkt ATS tespiti
        ats = detect_ats_from_url(career_url)

        if not ats:
            # URL'den tespit edilemedi → sayfaya gidip ATS URL'si bul
            actual_url, ats = _find_ats_url_in_page(career_url)
            if actual_url and actual_url != career_url:
                career_url = actual_url  # Gerçek ATS URL'sine geç

        jobs = []
        if ats == "teamtailor":
            jobs = scrape_teamtailor(career_url, name, logo)
        elif ats == "lever":
            jobs = scrape_lever(career_url, name, logo)
        elif ats == "greenhouse":
            jobs = scrape_greenhouse(career_url, name, logo)
        elif ats == "workable":
            jobs = scrape_workable(career_url, name, logo)
        elif ats:
            jobs = scrape_generic(career_url, name, logo, source=ats)
        else:
            jobs = scrape_generic(career_url, name, logo)

        if jobs:
            return jobs, f"✅ {len(jobs)} ilan ({ats or 'web'})"

    # ── Adım 3: Kariyer.net fallback ──────────────────────────────────────────
    kn_jobs = scrape_kariyer_net_fallback(name, logo)
    if kn_jobs:
        return kn_jobs, f"✅ {len(kn_jobs)} ilan (kariyer.net)"

    return [], "⚪ İlan bulunamadı"


# ════════════════════════════════════════════════════════════════════════════════
# Toplu Çalıştırma
# ════════════════════════════════════════════════════════════════════════════════

def run_smart_scraper(
    companies_file: Path | None = None,
    max_workers: int = 1,
    delay: float = 0.8,
) -> list[dict]:
    """
    Tüm firmalar için akıllı scraper'ı çalıştırır.
    """
    if companies_file is None:
        companies_file = SCRIPT_DIR / "companies.json"

    with open(companies_file, "r", encoding="utf-8") as f:
        companies = json.load(f)

    all_jobs = []
    seen = set()
    stats = {"found": 0, "not_found": 0, "errors": 0}

    console.print(f"\n[bold cyan]🧠 Akıllı Kariyer Sayfası Tarayıcı[/bold cyan]")
    console.print(f"[dim]{len(companies)} firma • Kariyer sayfası otomatik keşfediliyor[/dim]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=30),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("[green]{task.completed}/{task.total}"),
        console=console,
    ) as progress:
        task = progress.add_task("Taranıyor...", total=len(companies))

        for company in companies:
            progress.update(task, description=f"[cyan]{company['name'][:35]}...")

            try:
                jobs, status = smart_scrape_company(company)

                if jobs:
                    for j in jobs:
                        key = f"{j['company'].lower()}:{j['title'].lower()}"
                        if key not in seen:
                            seen.add(key)
                            all_jobs.append(j)
                    stats["found"] += 1
                    if len(jobs) > 0:
                        console.log(f"  ✅ [bold]{company['name']}[/bold]: {status}")
                else:
                    stats["not_found"] += 1

            except Exception as e:
                stats["errors"] += 1
                console.log(f"  ❌ {company['name']}: {str(e)[:50]}")

            progress.advance(task)
            time.sleep(delay)

    console.print(f"\n[bold green]✅ Tamamlandı![/bold green]")
    console.print(f"  📊 İlan bulunan firma: {stats['found']}")
    console.print(f"  📭 İlan bulunamayan: {stats['not_found']}")
    console.print(f"  ❌ Hata: {stats['errors']}")
    console.print(f"  🎯 Toplam benzersiz ilan: {len(all_jobs)}")

    return all_jobs


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Akıllı Kariyer Sayfası Tarayıcı")
    parser.add_argument("--test", metavar="URL",
                        help="Tek bir firma web sitesini test et")
    parser.add_argument("--company", metavar="ADI",
                        help="Test için firma adı")
    args = parser.parse_args()

    if args.test:
        name = args.company or "Test Firması"
        console.print(f"\n[cyan]🔍 Test: {name} → {args.test}[/cyan]")

        career = find_career_page(args.test)
        console.print(f"  Kariyer sayfası: [green]{career or 'Bulunamadı'}[/green]")

        if career:
            ats = detect_ats_from_url(career)
            console.print(f"  ATS platformu: [yellow]{ats or 'Bilinmiyor'}[/yellow]")

            company_dict = {
                "name": name,
                "url": args.test,
                "career_url": career,
                "logo": "🏢",
            }
            jobs, status = smart_scrape_company(company_dict)
            console.print(f"  Sonuç: {status}")
            for j in jobs[:5]:
                console.print(f"    - [green]{j['title']}[/green]")
    else:
        # Tam tarama
        from scraper import save_results
        jobs = run_smart_scraper()
        if jobs:
            jp, hp = save_results(jobs)
            console.print(f"\n[cyan]📄 JSON: {jp}[/cyan]")
            console.print(f"[cyan]🌐 HTML: {hp}[/cyan]")
            console.print(f"[bold]open {hp}[/bold]")
