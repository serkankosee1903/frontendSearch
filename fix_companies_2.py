import json
from urllib.parse import urlparse

with open('companies.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

count = 0
for comp in data:
    if 'career_url' in comp:
        c_url = comp['career_url'].rstrip('/')
        url = comp['url'].rstrip('/')
        
        # If the career_url is basically the same as the main URL 
        # and doesn't have obvious career keywords in the domain/path
        if c_url == url:
            career_keywords = ['career', 'kariyer', 'jobs', 'join', 'work']
            has_kw = any(kw in c_url.lower() for kw in career_keywords)
            if not has_kw:
                del comp['career_url']
                count += 1
        elif urlparse(c_url).path in ['', '/'] and urlparse(c_url).netloc == urlparse(url).netloc:
            # same domain, no path
             has_kw = any(kw in c_url.lower() for kw in ['career', 'kariyer', 'jobs', 'join', 'work'])
             if not has_kw:
                 del comp['career_url']
                 count += 1

with open('companies.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Removed redundant career_urls for {count} companies.")
