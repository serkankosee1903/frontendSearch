#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Türkiye Senior Front-End Developer İlan Bulucu v2
====================================================
Strateji:
  1. Kariyer.net'i doğrudan API ile tara (binlerce ilan, JS yok)
  2. LinkedIn public sayfalarını tara
  3. Statik firma listesindeki Teamtailor/Lever firmalarını tara
  4. Yeni firmaları discover_companies.py ile keşfet
"""

import json
import re
import time
import sys
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse, quote_plus
import hashlib

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel
from rich.text import Text
from jinja2 import Template

console = Console()

# ─── Yapılandırma ────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent
COMPANIES_FILE = SCRIPT_DIR / "companies.json"
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.google.com",
}

REQUEST_TIMEOUT = 15
DELAY = 1.0  # saniye

# ─── Filtre Kelimeleri ────────────────────────────────────────────────────────

SENIOR_FRONTEND_PATTERNS = [
    r"senior\s+front[\s\-]?end",
    r"kıdemli\s+front[\s\-]?end",
    r"sr\.?\s*front[\s\-]?end",
    r"lead\s+front[\s\-]?end",
    r"principal\s+front[\s\-]?end",
    r"senior\s+frontend",
    r"kıdemli\s+frontend",
    r"senior\s+ui\s+(developer|engineer|dev)",
    r"senior\s+react(\.?js)?\s*(developer|engineer|dev)",
    r"senior\s+vue(\.?js)?\s*(developer|engineer|dev)",
    r"senior\s+angular\s*(developer|engineer|dev)",
    r"senior\s+javascript\s*(developer|engineer|dev)",
    r"senior\s+typescript\s*(developer|engineer|dev)",
    r"senior\s+web\s+(developer|engineer|dev)",
    r"lead\s+ui\s*(developer|engineer)",
    r"staff\s+front[\s\-]?end",
    r"kıdemli\s+react",
    r"kıdemli\s+javascript",
    r"kıdemli\s+web\s+geliştirici",
    r"senior\s+next\.?js",
    r"senior\s+nuxt\.?js",
]

FRONTEND_KEYWORDS = [
    "frontend", "front-end", "front end",
    "react", "reactjs", "react.js",
    "vue", "vuejs", "vue.js",
    "angular", "angularjs",
    "nextjs", "next.js",
    "nuxtjs", "nuxt.js",
    "javascript", "typescript",
    "ui developer", "ui engineer",
    "web developer", "web engineer",
    "web geliştirici",
]

SENIOR_INDICATORS = [
    "senior", "sr.", "sr ", "kıdemli", "lead", "principal", "staff", "head of"
]

EXCLUDE_PATTERNS = [
    r"junior", r"jr\.", r"intern", r"stajyer", r"entry.level",
    r"\bbackend\b", r"\bback.end\b", r"\bback end\b",
    r"\bdevops\b", r"\bmobile\s+developer\b", r"\bandroid\b", r"\bios\s+dev",
    r"\bdata\s+scientist\b", r"\bmachine\s+learning\b",
    r"\bqa\s+engineer\b", r"\btest\s+engineer\b",
    r"\bproduct\s+manager\b", r"\bscrum\s+master\b",
    r"\bgraphic\s+designer\b", r"\bux\s+designer\b",
]


def is_senior_frontend(title: str) -> bool:
    t = title.lower().strip()
    # Önce hariç tut
    if any(re.search(p, t) for p in EXCLUDE_PATTERNS):
        return False
    # Frontend kelimeleri geçmesi yeterli (Senior olması şart değil)
    has_fe = any(kw in t for kw in FRONTEND_KEYWORDS)
    return has_fe or any(re.search(p, t) for p in SENIOR_FRONTEND_PATTERNS)


def clean(text: str) -> str:
    return " ".join(text.strip().split()) if text else ""


def uid(company: str, title: str) -> str:
    return hashlib.md5(f"{company}:{title}".lower().encode()).hexdigest()[:8]


def get(url: str, **kwargs) -> requests.Response | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT,
                         allow_redirects=True, **kwargs)
        r.raise_for_status()
        return r
    except requests.exceptions.SSLError:
        try:
            r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT,
                             allow_redirects=True, verify=False, **kwargs)
            r.raise_for_status()
            return r
        except Exception:
            return None
    except Exception:
        return None


def make_job(company: str, logo: str, title: str, url: str,
             location: str = "Türkiye", dept: str = "Engineering",
             tags: list = None, source: str = "web") -> dict:
    return {
        "id": uid(company, title),
        "company": company,
        "logo": logo,
        "title": clean(title),
        "url": url,
        "location": location or "Türkiye",
        "department": dept,
        "tags": tags or [],
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
    }


# ════════════════════════════════════════════════════════════════════════════════
# KAYNAK 1: Kariyer.net — Türkiye'nin en büyük iş ilanı platformu
# ════════════════════════════════════════════════════════════════════════════════

class KariyerNetSource:
    """
    Kariyer.net'i birden fazla arama sorgusu ile tarar.
    Bu site JS gerektirmez, doğrudan HTML döndürür.
    """

    BASE = "https://www.kariyer.net"
    SEARCHES = [
        "frontend+developer",
        "front-end+developer",
        "react+developer",
        "vue+developer",
        "angular+developer",
        "javascript+developer",
        "typescript+developer",
        "ui+developer",
        "web+developer",
        "nextjs+developer",
        "senior+frontend+developer",
        "senior+react+developer",
    ]

    def scrape(self) -> list[dict]:
        jobs = []
        seen = set()

        for query in self.SEARCHES:
            for page in range(1, 8):  # Her sorgu için max 7 sayfa (~350 ilan)
                url = (
                    f"{self.BASE}/is-ilani?"
                    f"pozisyon={query}"
                    f"&lokasyon=t%C3%BCrkiye"
                    f"&page={page}"
                )
                resp = get(url)
                if not resp:
                    break

                soup = BeautifulSoup(resp.text, "lxml")
                items = self._parse_page(soup)

                if not items:
                    break  # Bu sayfada ilan yok, sonraki sorguya geç

                new_count = 0
                for item in items:
                    key = f"{item['company']}:{item['title']}".lower()
                    if key not in seen:
                        seen.add(key)
                        jobs.append(item)
                        new_count += 1

                if new_count == 0:
                    break  # Tüm ilanlar zaten görüldü

                time.sleep(DELAY)

        return jobs

    def _parse_page(self, soup: BeautifulSoup) -> list[dict]:
        jobs = []

        # Kariyer.net ilan kartları — farklı HTML yapılarını dene
        selectors = [
            ".list-items-inner .list-item",
            ".job-list-item",
            "[class*='position-list'] li",
            "article[class*='job']",
            ".k-card",
        ]

        cards = []
        for sel in selectors:
            cards = soup.select(sel)
            if cards:
                break

        # Fallback: tüm <article> veya <li> içindeki iş ilanı linkleri
        if not cards:
            for a in soup.select("a[href*='/is-ilani/']"):
                title = clean(a.get_text())
                if not title or len(title) < 4:
                    continue
                if is_senior_frontend(title):
                    href = a["href"]
                    if not href.startswith("http"):
                        href = urljoin(self.BASE, href)
                    jobs.append(make_job(
                        company="Kariyer.net İlanı",
                        logo="🌐",
                        title=title,
                        url=href,
                        source="kariyer.net",
                    ))
            return jobs

        for card in cards:
            try:
                # Pozisyon başlığı
                title_el = card.select_one(
                    ".position-title, .job-title, h2.title, h3.title, "
                    "a.job-title, [class*='position-name'], [class*='job-name']"
                )
                # Şirket
                company_el = card.select_one(
                    ".company-name, .employer-name, .firm-name, "
                    "[class*='company'], [class*='employer']"
                )
                # Konum
                location_el = card.select_one(
                    ".location, .city, [class*='location'], [class*='city']"
                )
                # Link
                link_el = card.select_one("a[href*='/is-ilani/'], a.title, h2 a, h3 a")

                title = clean(title_el.get_text()) if title_el else ""
                company = clean(company_el.get_text()) if company_el else "Bilinmiyor"
                location = clean(location_el.get_text()) if location_el else "Türkiye"
                href = ""
                if link_el:
                    href = link_el.get("href", "")
                    if href and not href.startswith("http"):
                        href = urljoin(self.BASE, href)
                    # Başlık yoksa link metninden al
                    if not title:
                        title = clean(link_el.get_text())

                if not title or len(title) < 4:
                    continue

                if is_senior_frontend(title):
                    jobs.append(make_job(
                        company=company,
                        logo="🌐",
                        title=title,
                        url=href or url,
                        location=location,
                        source="kariyer.net",
                    ))
            except Exception:
                continue

        return jobs


# ════════════════════════════════════════════════════════════════════════════════
# KAYNAK 2: LinkedIn Turkey (public, auth gerekmez)
# ════════════════════════════════════════════════════════════════════════════════

class LinkedInSource:
    SEARCHES = [
        "frontend+developer",
        "react+developer",
        "vue+developer",
        "angular+developer",
        "javascript+developer",
        "ui+developer",
        "senior+frontend+developer",
    ]

    def scrape(self) -> list[dict]:
        jobs = []
        seen = set()

        for query in self.SEARCHES:
            url = (
                f"https://www.linkedin.com/jobs/search/?"
                f"keywords={query}"
                f"&location=Turkey"
                f"&f_TPR=r2592000"  # Son 30 gün
                f"&f_E=4"  # Senior level
            )
            resp = get(url)
            if not resp:
                time.sleep(DELAY)
                continue

            soup = BeautifulSoup(resp.text, "lxml")
            for card in soup.select(".base-card, .job-search-card, [data-entity-urn]"):
                try:
                    title_el = card.select_one(
                        ".base-search-card__title, h3.base-search-card__title, "
                        ".job-search-card__title"
                    )
                    company_el = card.select_one(
                        ".base-search-card__subtitle, h4.base-search-card__subtitle"
                    )
                    location_el = card.select_one(".job-search-card__location")
                    link_el = card.select_one("a.base-card__full-link, a[href*='/jobs/']")

                    title = clean(title_el.get_text()) if title_el else ""
                    company = clean(company_el.get_text()) if company_el else "LinkedIn"
                    location = clean(location_el.get_text()) if location_el else "Türkiye"
                    href = link_el["href"] if link_el else url

                    if not title or len(title) < 4:
                        continue

                    key = f"{company}:{title}".lower()
                    if key in seen:
                        continue
                    seen.add(key)

                    if is_senior_frontend(title):
                        jobs.append(make_job(
                            company=company,
                            logo="💼",
                            title=title,
                            url=href,
                            location=location,
                            source="linkedin",
                        ))
                except Exception:
                    continue

            time.sleep(DELAY * 2)  # LinkedIn'e daha az istek

        return jobs


# ════════════════════════════════════════════════════════════════════════════════
# KAYNAK 3: Teamtailor JSON API (tüm teamtailor firmaları için çalışır)
# ════════════════════════════════════════════════════════════════════════════════

class TeamtailorSource:
    def __init__(self, company: dict):
        self.company = company
        self.name = company["name"]
        self.url = company["career_url"]
        self.logo = company.get("logo", "🏢")

    def scrape(self) -> list[dict]:
        jobs = []
        parsed = urlparse(self.url)
        base = f"{parsed.scheme}://{parsed.netloc}"

        # Teamtailor JSON API denemesi
        api_url = f"{base}/jobs.json"
        resp = get(api_url)
        if resp:
            try:
                data = resp.json()
                job_list = data if isinstance(data, list) else data.get("jobs", [])
                for job in job_list:
                    title = job.get("title", "") or job.get("name", "")
                    if title and is_senior_frontend(title):
                        jobs.append(make_job(
                            company=self.name,
                            logo=self.logo,
                            title=title,
                            url=job.get("absolute_url", job.get("url", self.url)),
                            location=job.get("location", {}).get("name", "Türkiye") if isinstance(job.get("location"), dict) else "Türkiye",
                            source="teamtailor",
                        ))
                if jobs:
                    return jobs
            except Exception:
                pass

        # HTML fallback
        resp = get(self.url)
        if not resp:
            return jobs

        soup = BeautifulSoup(resp.text, "lxml")
        for a in soup.find_all("a", href=True):
            title = clean(a.get_text())
            if not title or len(title) < 4:
                continue
            href = a["href"]
            if "/jobs/" in href or "/positions/" in href or "job" in href.lower():
                if not href.startswith("http"):
                    href = urljoin(base, href)
                if is_senior_frontend(title):
                    jobs.append(make_job(
                        company=self.name,
                        logo=self.logo,
                        title=title,
                        url=href,
                        source="teamtailor",
                    ))

        return jobs


# ════════════════════════════════════════════════════════════════════════════════
# KAYNAK 4: Lever JSON API
# ════════════════════════════════════════════════════════════════════════════════

class LeverSource:
    def __init__(self, company: dict):
        self.company = company
        self.name = company["name"]
        self.url = company["career_url"]
        self.logo = company.get("logo", "🏢")

    def scrape(self) -> list[dict]:
        jobs = []
        api_url = self.url.rstrip("/") + "?format=json"
        resp = get(api_url)
        if resp:
            try:
                data = resp.json()
                for job in data:
                    title = job.get("text", "") or job.get("title", "")
                    if title and is_senior_frontend(title):
                        cats = job.get("categories", {})
                        location = cats.get("location", "Türkiye") if isinstance(cats, dict) else "Türkiye"
                        team = cats.get("team", "Engineering") if isinstance(cats, dict) else "Engineering"
                        jobs.append(make_job(
                            company=self.name,
                            logo=self.logo,
                            title=title,
                            url=job.get("hostedUrl", self.url),
                            location=location,
                            dept=team,
                            source="lever",
                        ))
                return jobs
            except Exception:
                pass

        # HTML fallback — Lever sayfasını parse et
        resp = get(self.url)
        if not resp:
            return jobs
        soup = BeautifulSoup(resp.text, "lxml")

        # Lever'ın standart .posting yapısı
        postings = soup.select(".posting")
        if postings:
            for posting in postings:
                title_el = posting.select_one(".posting-title h5, h5.posting-title, .posting-title")
                link_el = posting.select_one("a[href*='/jobs/']") or posting.find("a", href=True)
                location_el = posting.select_one(".sort-by-location, .posting-categories .sort-by-location")

                title = clean(title_el.get_text()) if title_el else ""
                if not title and link_el:
                    title = clean(link_el.get_text())
                location = clean(location_el.get_text()) if location_el else "Türkiye"
                href = link_el["href"] if link_el else self.url
                if href and not href.startswith("http"):
                    href = urljoin(self.url, href)

                if title and is_senior_frontend(title):
                    jobs.append(make_job(
                        company=self.name, logo=self.logo,
                        title=title, url=href,
                        location=location, source="lever",
                    ))
        else:
            # Genel fallback
            for a in soup.find_all("a", href=True):
                title = clean(a.get_text())
                if title and len(title) > 4 and is_senior_frontend(title):
                    href = a["href"]
                    if not href.startswith("http"):
                        href = urljoin(self.url, href)
                    jobs.append(make_job(
                        company=self.name, logo=self.logo,
                        title=title, url=href, source="lever",
                    ))
        return jobs


# ════════════════════════════════════════════════════════════════════════════════
# KAYNAK 5: Kariyer.net üzerinden firma bazlı ilanlar
# ════════════════════════════════════════════════════════════════════════════════

class KariyerNetCompanySource:
    """
    Kariyer.net'teki belirli bir firmanın ilanlarını çeker.
    JS gerektiren firma kariyer sayfaları için idealdir.
    """

    BASE = "https://www.kariyer.net"

    def __init__(self, company: dict):
        self.company = company
        self.name = company["name"]
        self.logo = company.get("logo", "🏢")

    def scrape(self) -> list[dict]:
        jobs = []
        url = f"{self.BASE}/is-ilani?firma={quote_plus(self.name)}"
        resp = get(url)
        if not resp:
            return jobs

        soup = BeautifulSoup(resp.text, "lxml")
        for a in soup.select("a[href*='/is-ilani/']"):
            title = clean(a.get_text())
            if not title or len(title) < 4:
                continue
            if is_senior_frontend(title):
                href = a["href"]
                if not href.startswith("http"):
                    href = urljoin(self.BASE, href)
                jobs.append(make_job(
                    company=self.name,
                    logo=self.logo,
                    title=title,
                    url=href,
                    source=f"kariyer.net/{self.name[:20]}",
                ))

        return jobs


# ════════════════════════════════════════════════════════════════════════════════
# Yardımcı: tekrar giderme + kaydetme
# ════════════════════════════════════════════════════════════════════════════════

def deduplicate(jobs: list[dict]) -> list[dict]:
    seen = set()
    result = []
    for j in jobs:
        key = f"{j['company'].lower()}:{j['title'].lower()}"
        if key not in seen:
            seen.add(key)
            result.append(j)
    return result


def save_results(jobs: list[dict]) -> tuple[Path, Path]:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = OUTPUT_DIR / f"ilanlar_{ts}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)

    latest = OUTPUT_DIR / "latest.json"
    with open(latest, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)

    html_path = generate_html(jobs)
    return json_path, html_path


def generate_html(jobs: list[dict]) -> Path:
    html_path = OUTPUT_DIR / "report.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(build_html(jobs))
    return html_path


def build_html(jobs: list[dict]) -> str:
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    companies_count = len(set(j["company"] for j in jobs))
    sources_count = len(set(j["source"].split("/")[0] for j in jobs))

    cards_html = ""
    for job in jobs:
        tags_html = "".join(f'<span class="tag">#{t}</span>' for t in job.get("tags", []))
        cards_html += f"""
        <div class="job-card" data-title="{job['title'].lower()}" data-company="{job['company'].lower()}" data-source="{job['source']}">
          <div class="card-header">
            <span class="logo">{job['logo']}</span>
            <div class="company-info">
              <span class="company-name">{job['company']}</span>
              <span class="source-badge">{job['source'].split('/')[0]}</span>
            </div>
          </div>
          <div class="job-title">{job['title']}</div>
          <div class="job-meta">
            <span class="meta-item">📍 {job['location']}</span>
            <span class="meta-item">💼 {job['department']}</span>
            {tags_html}
          </div>
          <a href="{job['url']}" target="_blank" rel="noopener" class="apply-btn">
            Başvur <span class="arrow">→</span>
          </a>
        </div>"""

    source_options = ""
    sources = sorted(set(j["source"].split("/")[0] for j in jobs))
    for s in sources:
        count = sum(1 for j in jobs if j["source"].split("/")[0] == s)
        source_options += f'<option value="{s}">{s} ({count})</option>'

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Senior Front-End İlanları Türkiye • {now}</title>
<meta name="description" content="Türkiye'deki yazılım firmalarından senior front-end developer ilanları">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  :root {{
    --bg: #0a0e1a;
    --bg2: #111827;
    --bg3: #1a2236;
    --border: #1e2d45;
    --text: #e2e8f0;
    --text-dim: #64748b;
    --accent: #3b82f6;
    --accent2: #10b981;
    --accent3: #8b5cf6;
    --danger: #ef4444;
    --gold: #f59e0b;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    line-height: 1.6;
  }}

  /* ── Header ── */
  .hero {{
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    border-bottom: 1px solid var(--border);
    padding: 3rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
  }}
  .hero::before {{
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% -30%, rgba(59,130,246,0.25) 0%, transparent 60%);
    pointer-events: none;
  }}
  .hero-badge {{
    display: inline-block;
    background: rgba(59,130,246,0.15);
    border: 1px solid rgba(59,130,246,0.3);
    color: #93c5fd;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.3rem 1rem;
    border-radius: 50px;
    margin-bottom: 1rem;
  }}
  .hero h1 {{
    font-size: clamp(1.8rem, 5vw, 3rem);
    font-weight: 700;
    background: linear-gradient(135deg, #e2e8f0, #93c5fd, #c4b5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.75rem;
  }}
  .hero p {{
    color: var(--text-dim);
    font-size: 1rem;
  }}

  /* ── Stats ── */
  .stats-bar {{
    display: flex;
    gap: 1px;
    background: var(--border);
    border-bottom: 1px solid var(--border);
  }}
  .stat {{
    flex: 1;
    background: var(--bg2);
    padding: 1.25rem;
    text-align: center;
  }}
  .stat .num {{
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--accent);
    display: block;
    line-height: 1;
  }}
  .stat .label {{
    font-size: 0.75rem;
    color: var(--text-dim);
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }}

  /* ── Toolbar ── */
  .toolbar {{
    background: var(--bg2);
    border-bottom: 1px solid var(--border);
    padding: 1rem 2rem;
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(10px);
  }}
  .search-box {{
    flex: 1;
    min-width: 250px;
    position: relative;
  }}
  .search-box input {{
    width: 100%;
    background: var(--bg3);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 0.625rem 1rem 0.625rem 2.5rem;
    border-radius: 8px;
    font-size: 0.9rem;
    font-family: inherit;
    outline: none;
    transition: border-color 0.2s;
  }}
  .search-box input:focus {{ border-color: var(--accent); }}
  .search-icon {{
    position: absolute;
    left: 0.75rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-dim);
    pointer-events: none;
  }}
  .filter-select {{
    background: var(--bg3);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 0.625rem 1rem;
    border-radius: 8px;
    font-size: 0.875rem;
    font-family: inherit;
    outline: none;
    cursor: pointer;
    transition: border-color 0.2s;
  }}
  .filter-select:focus {{ border-color: var(--accent); }}
  .result-count {{
    color: var(--text-dim);
    font-size: 0.875rem;
    white-space: nowrap;
  }}
  .result-count span {{ color: var(--accent); font-weight: 600; }}

  /* ── Grid ── */
  .container {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
  }}
  .job-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
    gap: 1.25rem;
  }}

  /* ── Card ── */
  .job-card {{
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    gap: 0.875rem;
  }}
  .job-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent2), var(--accent), var(--accent3));
    opacity: 0;
    transition: opacity 0.2s;
  }}
  .job-card:hover {{
    transform: translateY(-4px);
    border-color: rgba(59,130,246,0.35);
    box-shadow: 0 12px 40px rgba(0,0,0,0.4), 0 0 0 1px rgba(59,130,246,0.1);
  }}
  .job-card:hover::before {{ opacity: 1; }}

  .card-header {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }}
  .logo {{
    font-size: 1.75rem;
    line-height: 1;
    flex-shrink: 0;
  }}
  .company-info {{
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    flex: 1;
    min-width: 0;
  }}
  .company-name {{
    font-weight: 600;
    color: var(--text);
    font-size: 0.9rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .source-badge {{
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #60a5fa;
    background: rgba(59,130,246,0.12);
    border: 1px solid rgba(59,130,246,0.2);
    padding: 1px 7px;
    border-radius: 50px;
    align-self: flex-start;
  }}
  .job-title {{
    font-size: 1rem;
    font-weight: 600;
    color: #34d399;
    line-height: 1.4;
    flex: 1;
  }}
  .job-meta {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
  }}
  .meta-item {{
    font-size: 0.75rem;
    color: var(--text-dim);
    background: var(--bg3);
    padding: 3px 8px;
    border-radius: 4px;
    border: 1px solid var(--border);
  }}
  .tag {{
    font-size: 0.7rem;
    color: #a78bfa;
    background: rgba(139,92,246,0.1);
    border: 1px solid rgba(139,92,246,0.2);
    padding: 2px 7px;
    border-radius: 4px;
  }}
  .apply-btn {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.625rem 1.25rem;
    background: linear-gradient(135deg, #059669, #10b981);
    color: #fff;
    text-decoration: none;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 600;
    transition: opacity 0.15s, transform 0.15s;
    margin-top: auto;
  }}
  .apply-btn:hover {{ opacity: 0.9; transform: scale(1.02); }}
  .arrow {{ transition: transform 0.15s; }}
  .apply-btn:hover .arrow {{ transform: translateX(4px); }}

  /* ── Empty state ── */
  .empty {{
    grid-column: 1/-1;
    text-align: center;
    padding: 5rem 2rem;
    color: var(--text-dim);
  }}
  .empty h2 {{ font-size: 1.5rem; margin-bottom: 0.5rem; color: var(--text); }}

  /* ── Footer ── */
  footer {{
    text-align: center;
    padding: 2rem;
    color: var(--text-dim);
    font-size: 0.8rem;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
  }}

  @media (max-width: 640px) {{
    .stats-bar {{ flex-wrap: wrap; }}
    .stat {{ min-width: 50%; }}
    .hero {{ padding: 2rem 1rem; }}
    .container {{ padding: 1rem; }}
    .job-grid {{ grid-template-columns: 1fr; }}
    .toolbar {{ padding: 0.75rem 1rem; }}
  }}
</style>
</head>
<body>

<div class="hero">
  <div class="hero-badge">🔍 Otomatik Tarama</div>
  <h1>Senior Front-End Developer İlanları</h1>
  <p>Türkiye'deki yazılım firmalarının kariyer sayfaları ve iş platformları • {now}</p>
</div>

<div class="stats-bar">
  <div class="stat">
    <span class="num" id="totalCount">{len(jobs)}</span>
    <span class="label">Toplam İlan</span>
  </div>
  <div class="stat">
    <span class="num">{companies_count}</span>
    <span class="label">Farklı Şirket</span>
  </div>
  <div class="stat">
    <span class="num">{sources_count}</span>
    <span class="label">Kaynak Platform</span>
  </div>
  <div class="stat">
    <span class="num">{now.split()[0]}</span>
    <span class="label">Güncelleme</span>
  </div>
</div>

<div class="toolbar">
  <div class="search-box">
    <span class="search-icon">🔍</span>
    <input type="text" id="searchInput" placeholder="Pozisyon veya şirket ara..." oninput="filterJobs()">
  </div>
  <select class="filter-select" id="sourceFilter" onchange="filterJobs()">
    <option value="">Tüm Kaynaklar</option>
    {source_options}
  </select>
  <div class="result-count">Gösterilen: <span id="shownCount">{len(jobs)}</span> ilan</div>
</div>

<div class="container">
  <div class="job-grid" id="jobGrid">
    {cards_html if jobs else '<div class="empty"><h2>📭 Ilan Bulunamadı</h2><p>Scraper\'ı tekrar çalıştırın: <code>python scraper.py</code></p></div>'}
  </div>
  <div class="empty" id="emptyState" style="display:none;">
    <h2>😔 Sonuç bulunamadı</h2>
    <p>Arama kriterlerini değiştirin.</p>
  </div>
</div>

<footer>
  🤖 ilanSearch v2 • Otomatik oluşturuldu: {now} •
  <a href="latest.json" style="color:#60a5fa">JSON olarak indir</a>
</footer>

<script>
const cards = [...document.querySelectorAll('.job-card')];

function filterJobs() {{
  const q = document.getElementById('searchInput').value.toLowerCase().trim();
  const src = document.getElementById('sourceFilter').value;
  let shown = 0;

  cards.forEach(c => {{
    const titleMatch = !q || c.dataset.title.includes(q) || c.dataset.company.includes(q);
    const srcMatch = !src || c.dataset.source.startsWith(src);
    const visible = titleMatch && srcMatch;
    c.style.display = visible ? '' : 'none';
    if (visible) shown++;
  }});

  document.getElementById('shownCount').textContent = shown;
  document.getElementById('emptyState').style.display = shown === 0 ? 'flex' : 'none';
}}
</script>

</body>
</html>"""


# ════════════════════════════════════════════════════════════════════════════════
# Ana akış
# ════════════════════════════════════════════════════════════════════════════════

def load_companies() -> list[dict]:
    with open(COMPANIES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def print_table(jobs: list[dict]):
    if not jobs:
        console.print(Panel(
            "[yellow]Hiç ilan bulunamadı.[/yellow]\n"
            "[dim]Kariyer.net yapısı değişmiş olabilir. "
            "output/report.html'i kontrol edin.[/dim]",
            title="📭 Sonuç Yok", border_style="yellow"
        ))
        return

    t = Table(
        title=f"🎯 Bulunan İlanlar ({len(jobs)})",
        border_style="bright_blue",
        header_style="bold cyan",
        show_lines=True,
    )
    t.add_column("#", width=4, style="dim")
    t.add_column("Şirket", min_width=20, style="bold white")
    t.add_column("Pozisyon", min_width=32, style="bright_green")
    t.add_column("Kaynak", min_width=12, style="cyan")
    t.add_column("Konum", min_width=10, style="yellow")

    for i, j in enumerate(jobs, 1):
        t.add_row(
            str(i),
            f"{j['logo']} {j['company']}",
            j["title"],
            j["source"].split("/")[0],
            j["location"],
        )
    console.print(t)


def main():
    console.print(Panel(
        "[bold cyan]🚀 Senior Front-End Developer İlan Bulucu v2[/bold cyan]\n"
        "[dim]Kariyer.net + LinkedIn + 150+ firma kariyer sayfası[/dim]",
        border_style="bright_blue",
    ))

    all_jobs = []
    errors = []
    companies = load_companies()

    # Teamtailor ve Lever firmaları
    tt_companies = [c for c in companies if c.get("type") == "teamtailor"]
    lever_companies = [c for c in companies if c.get("type") == "lever"]
    other_companies = [c for c in companies if c.get("type") not in ("teamtailor", "lever")]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=25),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:

        # ── 1. Kariyer.net direkt arama ──────────────────────────────────────
        task = progress.add_task("[green]🌐 Kariyer.net taranıyor...", total=1)
        try:
            kn = KariyerNetSource()
            kn_jobs = kn.scrape()
            all_jobs.extend(kn_jobs)
            console.log(f"  ✅ Kariyer.net: {len(kn_jobs)} ilan bulundu")
        except Exception as e:
            errors.append(("Kariyer.net", str(e)))
            console.log(f"  ⚠️  Kariyer.net hatası: {e}")
        progress.advance(task)

        # ── 2. LinkedIn ──────────────────────────────────────────────────────
        task2 = progress.add_task("[blue]💼 LinkedIn taranıyor...", total=1)
        try:
            li = LinkedInSource()
            li_jobs = li.scrape()
            all_jobs.extend(li_jobs)
            console.log(f"  ✅ LinkedIn: {len(li_jobs)} ilan bulundu")
        except Exception as e:
            errors.append(("LinkedIn", str(e)))
        progress.advance(task2)

        # ── 3. Teamtailor firmalar ────────────────────────────────────────────
        task3 = progress.add_task(
            f"[cyan]🏢 {len(tt_companies)} Teamtailor firma...",
            total=len(tt_companies)
        )
        for c in tt_companies:
            progress.update(task3, description=f"[cyan]🔍 {c['name']}...")
            try:
                jobs = TeamtailorSource(c).scrape()
                if jobs:
                    all_jobs.extend(jobs)
                    console.log(f"  ✅ {c['name']}: {len(jobs)} ilan")
            except Exception as e:
                errors.append((c["name"], str(e)))
            progress.advance(task3)
            time.sleep(DELAY)

        # ── 4. Lever firmalar ────────────────────────────────────────────────
        task4 = progress.add_task(
            f"[magenta]🎯 {len(lever_companies)} Lever firma...",
            total=len(lever_companies)
        )
        for c in lever_companies:
            progress.update(task4, description=f"[magenta]🔍 {c['name']}...")
            try:
                jobs = LeverSource(c).scrape()
                if jobs:
                    all_jobs.extend(jobs)
                    console.log(f"  ✅ {c['name']}: {len(jobs)} ilan")
            except Exception as e:
                errors.append((c["name"], str(e)))
            progress.advance(task4)
            time.sleep(DELAY)

        # ── 5. Kariyer.net üzerinden custom firmalar ──────────────────────────
        task5 = progress.add_task(
            f"[yellow]🔎 {len(other_companies)} özel firma (Kariyer.net)...",
            total=len(other_companies)
        )
        for c in other_companies:
            progress.update(task5, description=f"[yellow]🔎 {c['name']} (Kariyer.net)...")
            try:
                jobs = KariyerNetCompanySource(c).scrape()
                if jobs:
                    all_jobs.extend(jobs)
                    console.log(f"  ✅ {c['name']}: {len(jobs)} ilan")
            except Exception as e:
                errors.append((c["name"], str(e)))
            progress.advance(task5)
            time.sleep(DELAY * 0.5)

    # Tekrar gider + sırala
    unique = deduplicate(all_jobs)
    unique.sort(key=lambda j: (j["source"], j["company"]))

    # Tablo göster
    console.print()
    print_table(unique)

    # Kaydet
    if unique:
        jp, hp = save_results(unique)
        console.print(f"\n[bold green]✅ {len(unique)} ilan kaydedildi![/bold green]")
        console.print(f"  📄 JSON  : [cyan]{jp}[/cyan]")
        console.print(f"  🌐 HTML  : [cyan]{hp}[/cyan]")
        console.print(f"\n[dim]HTML raporu açmak için:[/dim] [bold]open {hp}[/bold]")
    else:
        console.print("\n[yellow]⚠️  Hiç ilan bulunamadı.[/yellow]")
        console.print("[dim]HTML rapor güncellendi. Sonraki taramada çıkabilir.[/dim]")

    if errors:
        console.print(f"\n[dim]⚠️  {len(errors)} kaynakta küçük hatalar (bant genişliği sınırı vs.):[/dim]")
        for n, e in errors[:3]:
            console.print(f"  [dim]• {n}: {str(e)[:60]}[/dim]")

    return unique


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]İptal edildi.[/yellow]")
