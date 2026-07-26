import os
import requests

TOKEN = os.getenv("GITHUB_TOKEN", "")  # JANGAN hardcode token! Set via env variable
headers = {"Authorization": f"token {TOKEN}", "User-Agent": "Mozilla/5.0"}

print("=== SEMUA REPO PUNYA WINAR ===")
r = requests.get("https://api.github.com/user/repos?per_page=100", headers=headers)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    for repo in r.json():
        print(repo["full_name"], "-", repo.get("description", "-"))
        print(f"  URL: {repo['html_url']}, Default branch: {repo['default_branch']}")
        print(f"  Updated: {repo['updated_at']}")
        print()
else:
    print(r.text[:500])

print("\n=== CEK GITHUB ACTIONS ===")
# Cari repo yang ada workflow-nya
for repo in r.json() if r.status_code == 200 else []:
    wf = requests.get(f"https://api.github.com/repos/{repo['full_name']}/actions/workflows", headers=headers)
    if wf.status_code == 200 and wf.json().get("total_count", 0) > 0:
        print(f"\n{repo['full_name']} - Workflows ({wf.json()['total_count']})")
        for w in wf.json()["workflows"]:
            print(f"  [{'ACTIVE' if w['state']=='active' else w['state']}] {w['name']} - {w['path']}")
            print(f"  ID: {w['id']}")
        # Cek status runs terakhir
        runs = requests.get(f"https://api.github.com/repos/{repo['full_name']}/actions/runs?per_page=3", headers=headers)
        if runs.status_code == 200:
            for run in runs.json().get("workflow_runs", []):
                print(f"  -> Run #{run['run_number']}: {run['status']}/{run['conclusion']} ({run['updated_at']})")
