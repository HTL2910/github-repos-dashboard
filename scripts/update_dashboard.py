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
# Prefer personal token so we can write to the profile repo
TOKEN = os.getenv("PERSONAL_ACCESS_TOKEN") or os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("GITHUB_REPOSITORY", f"{OWNER}/github-repos-dashboard").split("/")[-1]

HEADERS = {"Accept": "application/vnd.github+json"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

# Topic → Category mapping
TOPIC_MAP = {
    "unity": "🎮 Unity / Game",
    "unity3d": "🎮 Unity / Game",
    "game": "🎮 Unity / Game",
    "gamedev": "🎮 Unity / Game",
    "shader": "🎮 Unity / Game",
    "ai": "🤖 AI / ML",
    "ml": "🤖 AI / ML",
    "machine-learning": "🤖 AI / ML",
    "deep-learning": "🤖 AI / ML",
    "llm": "🤖 AI / ML",
    "gpt": "🤖 AI / ML",
    "bot": "💬 Bot / Mini App",
    "zalo": "💬 Bot / Mini App",
    "miniapp": "💬 Bot / Mini App",
    "react": "🌐 Web / Frontend",
    "nextjs": "🌐 Web / Frontend",
    "frontend": "🌐 Web / Frontend",
    "web": "🌐 Web / Frontend",
}

# Language → Category mapping
LANGUAGE_MAP = {
    "c#": "🎮 Unity / Game",
    "shaderlab": "🎮 Unity / Game",
    "python": "🤖 AI / ML",
    "jupyter notebook": "🤖 AI / ML",
    "html": "🌐 Web / Frontend",
    "css": "🌐 Web / Frontend",
    "javascript": "🌐 Web / Frontend",
    "typescript": "🌐 Web / Frontend",
}

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
    # 1. Prefer GitHub Topics
    topics = [t.lower() for t in repo.get("topics") or []]
    for topic in topics:
        if topic in TOPIC_MAP:
            return TOPIC_MAP[topic]

    # 2. Language-based
    lang = (repo.get("language") or "").lower()
    if lang in LANGUAGE_MAP:
        return LANGUAGE_MAP[lang]

    # 3. Fallback to keyword matching
    name = (repo.get("name") or "").lower()
    desc = (repo.get("description") or "").lower()
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

    dashboard_url = f"https://{OWNER}.github.io/{REPO_NAME}/"
    source_url = f"https://github.com/{OWNER}/{REPO_NAME}"
    workflow_url = f"https://github.com/{OWNER}/{REPO_NAME}/actions/workflows/update-dashboard.yml"

    lines = [
        "<div align=\"center\">",
        "",
        f"# {OWNER}",
        "",
        f"**Repos Dashboard** — tự động cập nhật",
        "",
        f"[![Dashboard](https://img.shields.io/badge/📊_Xem_Dashboard_đầy_đủ-blue?style=for-the-badge)]({dashboard_url})",
        "",
        f"[![Update](https://img.shields.io/badge/🔄_Update_Profile-success?style=for-the-badge)]({workflow_url})",
        "",
        f"[![Source](https://img.shields.io/badge/🔧_Quản_lý_Dashboard-green?style=for-the-badge)]({source_url})",
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
        f"*Profile được tự động cập nhật từ [{REPO_NAME}]({source_url})*"
    ])
    return "\n".join(lines)

def update_profile_readme(content: str):
    if not os.getenv("PERSONAL_ACCESS_TOKEN"):
        print("No PERSONAL_ACCESS_TOKEN set, skip profile update")
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
        print("Profile README updated successfully")
    else:
        print(f"Profile update failed: {put.status_code} - {put.text[:300]}")

def generate_readme(repos):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    total = len(repos)
    private = sum(1 for r in repos if r.get("private"))
    public = total - private

    workflow_url = f"https://github.com/{OWNER}/{REPO_NAME}/actions/workflows/update-dashboard.yml"
    token_url = "https://github.com/settings/tokens/new?scopes=repo&description=github-repos-dashboard"
    secrets_url = f"https://github.com/{OWNER}/{REPO_NAME}/settings/secrets/actions"
    pages_url = f"https://{OWNER}.github.io/{REPO_NAME}/"
    profile_repo_url = f"https://github.com/new?name={OWNER}&description=Profile+README"
    profile_view_url = f"https://github.com/{OWNER}/{OWNER}"

    lines = [
        f"# 📊 GitHub Repos Dashboard - {OWNER}",
        "",
        "## 🚀 Hướng dẫn nhanh",
        "",
        f"[![0. Tạo Profile Repo](https://img.shields.io/badge/0._Tạo_Profile_Repo_(username/username)-purple?style=for-the-badge)]({profile_repo_url})",
        "",
        f"[![1. Get Token](https://img.shields.io/badge/1._Get_Personal_Access_Token-orange?style=for-the-badge)]({token_url})",
        "",
        f"[![2. Add Secret](https://img.shields.io/badge/2._Add_Secret_PERSONAL_ACCESS_TOKEN-yellow?style=for-the-badge)]({secrets_url})",
        "",
        f"[![3. Update Profile](https://img.shields.io/badge/3._Update_Profile_README-success?style=for-the-badge)]({workflow_url})",
        "",
        f"[![Xem Profile](https://img.shields.io/badge/👤_Xem_Profile_của_bạn-blue?style=for-the-badge)]({profile_view_url})",
        "",
        "> **Bước 0** → Tạo repo tên đúng username của bạn (nếu chưa có)  ",
        "> **Bước 1** → Tạo token (chọn scope `repo`)  ",
        "> **Bước 2** → Thêm secret tên đúng `PERSONAL_ACCESS_TOKEN`  ",
        "> **Bước 3** → Chạy workflow để cập nhật profile",
        "",
        f"**Dashboard web**: [{pages_url}]({pages_url})",
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
    print(f"Using personal token: {bool(os.getenv('PERSONAL_ACCESS_TOKEN'))}")
    repos = get_repos(OWNER)
    print(f"Found {len(repos)} repositories")

    readme = generate_readme(repos)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    print("README.md updated")

    profile_content = generate_profile_readme(repos)
    update_profile_readme(profile_content)
