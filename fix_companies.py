import json
from urllib.parse import urlparse

with open('companies.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

count = 0
for comp in data:
    if 'career_url' not in comp:
        # Move the job url to career_url
        comp['career_url'] = comp['url']
        # Try to clean up the url to just be the base domain if it has path
        parsed = urlparse(comp['url'])
        if parsed.path and parsed.path != '/':
            comp['url'] = f"{parsed.scheme}://{parsed.netloc}"
        count += 1

with open('companies.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Fixed {count} companies in companies.json")
