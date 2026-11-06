#!/usr/bin/env python3
"""
Generate GitHub repos dashboard for the current repository owner.
Also tries to update the user's profile README (username/username).
"""
import os
import requests
from datetime import datetime
from collections import defaultdict
import base64

OWNER = os.getenv("GITHUB_REPOSITORY_OWNER") or os.getenv("GITHUB_ACTOR") or "HTL2910"
TOKEN = os.getenv("GITHUB_TOKEN") or os.getenv("PERSONAL_ACCESS_TOKEN")
REPO_NAME = os.getenv("GITHUB_REPOSITORY", f"{OWNER}/github-repos-dashboard").split("/")[-1]

HEADERS = {"Accept": "application/vnd.github+json"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

def get_repos(username: str):
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/repos"
        params = {"per_page": 100, "page": page, "sort": "updated", "type": "owner"}
        resp = requests.get(url, headers=HEADERS, params=params)
        if resp.status_code != 200:
            print(f"Error fetching repos: {resp.status_code}")
            break
        data = resp.json()
        if not data:
            break
        repos.extend(data)
        page += 1
        if page > 10:
            break
    return repos

def categorize(repo):
    name = (repo.get("name") or "").lower()
    desc = (repo.get("description") or "").lower()
    lang = (repo.get("language") or "").lower()
    text = f"{name} {desc} {lang}"

    if any(k in text for k in ["unity", "game", "shader", "metroidvania", "platformer"]):
        return "🎮 Unity / Game"
    if any(k in text for k in ["ai", "ml", "machine", "learning", "gpt", "llm", "openai", "bedrock"]):
        return "🤖 AI / ML"
    if any(k in text for k in ["zalo", "bot", "miniapp", "mini-app"]):
        return "💬 Bot / Mini App"
    if any(k in text for k in ["react", "web", "frontend", "html", "css", "next"]):
        return "🌐 Web / Frontend"
    return "📁 Other"

def generate_profile_readme(repos):
    now = datetime.utcnow().strftime("%Y-%m-%d")
    total = len(repos)
    langs = {}
    for r in repos:
        if r.get("language"):
            langs[r["language"]] = langs.get(r["language"], 0) + 1
    top_langs = sorted(langs.items(), key=lambda x: -x[1])[:5]
    lang_badges = " ".join([f"`{l}`" for l, _ in top_langs])

    lines = [
        "<div align=\"center\">",
        "",
        f"# {OWNER}",
        "",
        f"**Repos Dashboard** — tự động cập nhật",
        "",
        f"[![Dashboard](https://img.shields.io/badge/📊_Xem_chi_tiết-blue?style=for-the-badge)](https://{OWNER}.github.io/{REPO_NAME}/)",
        "",
        "</div>",
        "",
        "---",
        "",
        f"**Tổng**: {total} repos  ",
        f"**Ngôn ngữ chính**: {lang_badges or '-'}  ",
        f"**Cập nhật**: {now}",
        "",
        "### Nhóm chính",
        ""
    ]

    groups = defaultdict(int)
    for r in repos:
        groups[categorize(r)] += 1
    for cat, count in sorted(groups.items(), key=lambda x: -x[1]):
        lines.append(f"- {cat}: **{count}**")

    lines.extend([
        "",
        "---",
        "",
        f"*Profile được tự động cập nhật từ [{REPO_NAME}](https://github.com/{OWNER}/{REPO_NAME})*"
    ])
    return "\n".join(lines)

def update_profile_readme(content: str):
    if not TOKEN:
        print("No token, skip profile update")
        return
    url = f"https://api.github.com/repos/{OWNER}/{OWNER}/contents/README.md"
    resp = requests.get(url, headers=HEADERS)
    sha = None
    if resp.status_code == 200:
        sha = resp.json().get("sha")

    payload = {
        "message": "chore: auto-update profile dashboard",
        "content": base64.b64encode(content.encode()).decode(),
        "branch": "main"
    }
    if sha:
        payload["sha"] = sha

    put = requests.put(url, headers=HEADERS, json=payload)
    if put.status_code in (200, 201):
        print("Profile README updated")
    else:
        print(f"Profile update failed: {put.status_code} - {put.text[:200]}")

def generate_readme(repos):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    total = len(repos)
    private = sum(1 for r in repos if r.get("private"))
    public = total - private

    workflow_url = f"https://github.com/{OWNER}/{REPO_NAME}/actions/workflows/update-dashboard.yml"
    token_url = "https://github.com/settings/tokens/new?scopes=repo&description=github-repos-dashboard"
    secrets_url = f"https://github.com/{OWNER}/{REPO_NAME}/settings/secrets/actions"

    lines = [
        f"# 📊 GitHub Repos Dashboard - {OWNER}",
        "",
        "## 🚀 Quick Actions",
        "",
        f"[![Get Token](https://img.shields.io/badge/🔑_Get_Personal_Access_Token-orange?style=for-the-badge)]({token_url})",
        "",
        f"[![Update Profile](https://img.shields.io/badge/✅_Update_Profile_README-success?style=for-the-badge)]({workflow_url})",
        "",
        "> **Bước 1**: Bấm nút Get Token → tạo token (scope `repo`)  ",
        f"> **Bước 2**: Vào [Secrets]({secrets_url}) → thêm secret tên `PERSONAL_ACCESS_TOKEN`  ",
        "> **Bước 3**: Bấm nút Update Profile README",
        "",
        f"**Cập nhật**: {now}  ",
        f"**Tổng**: {total} repos ({private} private / {public} public)",
        "",
        "---",
        ""
    ]

    groups = defaultdict(list)
    for r in repos:
        groups[categorize(r)].append(r)

    for cat in sorted(groups.keys()):
        lines.append(f"## {cat} ({len(groups[cat])})")
        lines.append("")
        lines.append("| Repo | Language | Updated | Stars | Visibility | Description |")
        lines.append("|------|----------|---------|-------|------------|-------------|")
        for r in sorted(groups[cat], key=lambda x: x.get("updated_at") or "", reverse=True)[:30]:
            name = r["name"]
            lang = r.get("language") or "-"
            updated = (r.get("updated_at") or "")[:10]
            stars = r.get("stargazers_count", 0)
            vis = "🔒" if r.get("private") else "🌐"
            desc = (r.get("description") or "-")[:60].replace("|", "/")
            url = r["html_url"]
            lines.append(f"| [{name}]({url}) | {lang} | {updated} | {stars} | {vis} | {desc} |")
        lines.append("")

    lines.extend([
        "---",
        "",
        "*Generated automatically*"
    ])
    return "\n".join(lines)

if __name__ == "__main__":
    print(f"Generating dashboard for: {OWNER}")
    repos = get_repos(OWNER)
    print(f"Found {len(repos)} repositories")

    readme = generate_readme(repos)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    print("README.md updated")

    profile_content = generate_profile_readme(repos)
    update_profile_readme(profile_content)
