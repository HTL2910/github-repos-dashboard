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
from urllib.parse import quote

OWNER = os.getenv("GITHUB_REPOSITORY_OWNER") or os.getenv("GITHUB_ACTOR") or "unknown"
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
    topics = [t.lower() for t in repo.get("topics") or []]
    for topic in topics:
        if topic in TOPIC_MAP:
            return TOPIC_MAP[topic]

    lang = (repo.get("language") or "").lower()
    if lang in LANGUAGE_MAP:
        return LANGUAGE_MAP[lang]

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
    cache_bust = datetime.utcnow().strftime("%Y%m%d%H%M")

    header_text = quote(OWNER)
    header_desc = quote("Developer · Open Source · Building cool things")
    header = f"![Header](https://capsule-render.vercel.app/api?type=waving&height=220&color=gradient&customColorList=6,12,20,24&text={header_text}&fontColor=ffffff&fontSize=40&fontAlignY=35&desc={header_desc}&descAlignY=55&animation=fadeIn)"

    typing = "[![Typing SVG](https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=22&duration=2800&pause=800&color=70A5FD&center=true&vCenter=true&repeat=true&width=750&lines=Building+projects+and+exploring+new+tech;Managing+repositories+with+this+dashboard;Open+to+collaboration)](https://git.io/typing-svg)"

    dashboard_url = f"https://{OWNER}.github.io/{REPO_NAME}/"
    source_url = f"https://github.com/{OWNER}/{REPO_NAME}"
    workflow_url = f"https://github.com/{OWNER}/{REPO_NAME}/actions/workflows/update-dashboard.yml"
    profile_views = f"https://komarev.com/ghpvc/?username={OWNER}&style=for-the-badge&color=7c3aed&label=PROFILE+VIEWS"

    snake_dark = f"https://raw.githubusercontent.com/{OWNER}/{OWNER}/output/github-contribution-grid-snake-dark.svg"

    stats_url = f"https://github-readme-stats.vercel.app/api?username={OWNER}&show_icons=true&theme=tokyonight&hide_border=true&bg_color=0d1117&cache_bust={cache_bust}"
    langs_url = f"https://github-readme-stats.vercel.app/api/top-langs/?username={OWNER}&layout=compact&theme=tokyonight&hide_border=true&bg_color=0d1117&cache_bust={cache_bust}"
    trophies_url = f"https://github-profile-trophy.vercel.app/?username={OWNER}&theme=tokyonight&no-frame=true&no-bg=true&margin-w=4&cache_bust={cache_bust}"

    lines = [
        "<div align=\"center\">",
        "",
        header,
        "",
        typing,
        "",
        f"<a href=\"https://github.com/{OWNER}\"><img src=\"https://img.shields.io/badge/GitHub-{OWNER}-181717?style=for-the-badge&logo=github&logoColor=white\"></a>",
        f"<a href=\"{dashboard_url}\"><img src=\"https://img.shields.io/badge/📊_View_Dashboard-blue?style=for-the-badge\"></a>",
        f"<img src=\"{profile_views}\">",
        "",
        "```text",
        f"📍 GitHub User: {OWNER}",
        "```",
        "",
        "</div>",
        "",
        "## `> whoami`",
        "",
        f"This profile is auto-generated by the [Repos Dashboard]({source_url}). It shows an overview of repositories, categories, and activity.",
        "",
        "```mermaid",
        "flowchart LR",
        "    REPOS[\"Your Repositories\"] --> DASH[\"Repos Dashboard\"]",
        "    DASH --> PROFILE[\"This Profile\"]",
        "```",
        "",
        "## `> toolchain`",
        "",
        "<div align=\"center\">",
        "",
        "### Languages & Tools",
        "",
        "![C#](https://img.shields.io/badge/C%23-239120?style=for-the-badge&logo=csharp&logoColor=white)",
        "![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)",
        "![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)",
        "![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)",
        "",
        "</div>",
        "",
        "## `> github stats`",
        "",
        "<div align=\"center\">",
        "",
        f"![GitHub Stats]({stats_url})",
        "",
        f"![Top Languages]({langs_url})",
        "",
        "</div>",
        "",
        "## `> trophies`",
        "",
        "<div align=\"center\">",
        "",
        f"![Trophies]({trophies_url})",
        "",
        "</div>",
        "",
        "## `> stats`",
        "",
        f"**Total repositories**: {total}  ",
        f"**Last updated**: {now}",
        "",
        "### Categories",
        ""
    ]

    groups = defaultdict(int)
    for r in repos:
        groups[categorize(r)] += 1
    for cat, count in sorted(groups.items(), key=lambda x: -x[1]):
        lines.append(f"- {cat}: **{count}**")

    lines.extend([
        "",
        "## `> recent repos`",
        "",
        "| Repo | Language | Updated | Stars | Category |",
        "|------|----------|---------|-------|----------|"
    ])
    recent = sorted(repos, key=lambda x: x.get("updated_at") or "", reverse=True)[:12]
    for r in recent:
        name = r["name"]
        lang = r.get("language") or "-"
        updated = (r.get("updated_at") or "")[:10]
        stars = r.get("stargazers_count", 0)
        cat = categorize(r)
        url = r["html_url"]
        lines.append(f"| [{name}]({url}) | {lang} | {updated} | {stars} | {cat} |")

    lines.extend([
        "",
        "## `> contribution snake`",
        "",
        "<div align=\"center\">",
        "",
        "<picture>",
        f"  <source media=\"(prefers-color-scheme: dark)\" srcset=\"{snake_dark}\">",
        f"  <img alt=\"Contribution snake\" src=\"{snake_dark}\">",
        "</picture>",
        "",
        "</div>",
        "",
        "<div align=\"center\">",
        "",
        f"[![Update Profile](https://img.shields.io/badge/🔄_Update_Profile-success?style=for-the-badge)]({workflow_url})",
        f"[![Manage Dashboard](https://img.shields.io/badge/🔧_Manage_Dashboard-green?style=for-the-badge)]({source_url})",
        "",
        "![Footer](https://capsule-render.vercel.app/api?type=waving&height=100&section=footer&color=gradient&customColorList=6,12,20,24&animation=fadeIn)",
        "",
        "</div>"
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
        "message": "chore: auto-update dynamic profile",
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
    pages_settings_url = f"https://github.com/{OWNER}/{REPO_NAME}/settings/pages"
    pages_url = f"https://{OWNER}.github.io/{REPO_NAME}/"
    profile_repo_url = f"https://github.com/new?name={OWNER}&description=Profile+README"
    profile_view_url = f"https://github.com/{OWNER}/{OWNER}"
    profile_actions_url = f"https://github.com/{OWNER}/{OWNER}/actions"
    actions_url = f"https://github.com/{OWNER}/{REPO_NAME}/actions"

    lines = [
        f"# 📊 GitHub Repos Dashboard - {OWNER}",
        "",
        "## 🚀 Detailed Setup Guide",
        "",
        "> **Note for forked users**: After forking, run the workflow on your fork so all links and content update to your username.",
        "",
        "### 1. Enable the workflow (required on forks)",
        "",
        f"[![Open Actions](https://img.shields.io/badge/Open_Actions-blue?style=for-the-badge)]({actions_url})",
        "",
        "1. Click **Update Repos Dashboard** in the left sidebar",
        "2. Click **Enable workflow** (if it shows as Disabled)",
        "",
        "### 2. Create your profile repository",
        "",
        f"[![Create Profile Repo](https://img.shields.io/badge/Create_Profile_Repo-purple?style=for-the-badge)]({profile_repo_url})",
        "",
        f"- Name must be exactly: **`{OWNER}`**",
        "- Visibility: **Public**",
        "",
        "### 3. Create a Personal Access Token",
        "",
        f"[![Get Token](https://img.shields.io/badge/Get_Token-orange?style=for-the-badge)]({token_url})",
        "",
        "- Select **Generate new token (classic)**",
        "- Check the **`repo`** scope",
        "- Copy the token immediately",
        "",
        "### 4. Add the token as a secret",
        "",
        f"[![Add Secret](https://img.shields.io/badge/Add_Secret-yellow?style=for-the-badge)]({secrets_url})",
        "",
        "- Name: `PERSONAL_ACCESS_TOKEN`",
        "- Paste your token as the value",
        "",
        "### 5. Enable GitHub Pages",
        "",
        f"[![Open Pages Settings](https://img.shields.io/badge/Open_Pages_Settings-blue?style=for-the-badge)]({pages_settings_url})",
        "",
        "1. Source: **Deploy from a branch**",
        "2. Branch: `main` / `/ (root)`",
        "3. Click **Save**",
        "",
        f"Dashboard will be available at: [{pages_url}]({pages_url})",
        "",
        "### 6. (Optional) Add Contribution Snake",
        "",
        "To show the animated contribution snake on your profile:",
        "",
        f"1. Go to your profile repo: [https://github.com/{OWNER}/{OWNER}](https://github.com/{OWNER}/{OWNER})",
        "2. Create file `.github/workflows/snake.yml` with this content:",
        "",
        "```yaml",
        "name: Generate Snake",
        "on:",
        "  schedule:",
        "    - cron: \"0 0 * * *\"",
        "  workflow_dispatch:",
        "jobs:",
        "  generate:",
        "    runs-on: ubuntu-latest",
        "    steps:",
        "      - uses: Platane/snk@v3",
        "        with:",
        f"          github_user_name: {OWNER}",
        "          outputs: |",
        "            dist/github-contribution-grid-snake.svg",
        "            dist/github-contribution-grid-snake-dark.svg?palette=github-dark",
        "      - uses: crazy-max/ghaction-github-pages@v4",
        "        with:",
        "          target_branch: output",
        "          build_dir: dist",
        "        env:",
        "          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}",
        "```",
        "",
        f"3. Go to [Actions]({profile_actions_url}) → run **Generate Snake**",
        "",
        "### 7. Run the dashboard workflow",
        "",
        f"[![Run Workflow](https://img.shields.io/badge/Run_Workflow-success?style=for-the-badge)]({workflow_url})",
        "",
        "This updates this README and your profile README.",
        "",
        "### 8. View your profile",
        "",
        f"[![View Profile](https://img.shields.io/badge/View_Profile-blue?style=for-the-badge)]({profile_view_url})",
        "",
        "---",
        "",
        f"**Web Dashboard**: [{pages_url}]({pages_url})",
        "",
        f"**Updated**: {now}  ",
        f"**Total**: {total} repos ({private} private / {public} public)",
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
        "*Generated automatically. Run the workflow to refresh.*"
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
