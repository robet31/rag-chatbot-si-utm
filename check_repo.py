import requests
import sys
import subprocess

# Cari repo automation milik user winar
print("=== Cari repo 'automation' punya winar ===")
r = requests.get('https://api.github.com/search/repositories?q=automation+user:winar',
                 headers={'User-Agent': 'Mozilla/5.0'})
if r.status_code == 200:
    data = r.json()
    print(f"Total: {data.get('total_count', 0)}")
    for repo in data.get('items', []):
        print(f"  {repo['full_name']}")
        print(f"  Desc: {repo.get('description', '-')}")
        print(f"  URL: {repo['html_url']}")
        print(f"  Default branch: {repo['default_branch']}")
        print()
else:
    print(f"Error: {r.status_code}")
    print(r.text[:500])

# Coba juga cari repo dengan nama mirip
print("\n=== Cari repo 'daily' punya winar ===")
r2 = requests.get('https://api.github.com/search/repositories?q=daily+user:winar',
                  headers={'User-Agent': 'Mozilla/5.0'})
if r2.status_code == 200:
    data = r2.json()
    print(f"Total: {data.get('total_count', 0)}")
    for repo in data.get('items', []):
        print(f"  {repo['full_name']}")
        print(f"  URL: {repo['html_url']}")
        print()
else:
    print(f"Error: {r2.status_code}")
