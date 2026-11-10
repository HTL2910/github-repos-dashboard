# 📊 GitHub Repos Dashboard - HTL2910

## 🚀 Detailed Setup Guide

> **Note for forked users**: After forking, run the workflow on your fork so all links and content update to your username.

### 1. Enable the workflow (required on forks)

[![Open Actions](https://img.shields.io/badge/Open_Actions-blue?style=for-the-badge)](https://github.com/HTL2910/github-repos-dashboard/actions)

1. Click **Update Repos Dashboard** in the left sidebar
2. Click **Enable workflow** (if it shows as Disabled)

### 2. Create your profile repository

[![Create Profile Repo](https://img.shields.io/badge/Create_Profile_Repo-purple?style=for-the-badge)](https://github.com/new?name=HTL2910&description=Profile+README)

- Name must be exactly: **`HTL2910`**
- Visibility: **Public**

### 3. Create a Personal Access Token

[![Get Token](https://img.shields.io/badge/Get_Token-orange?style=for-the-badge)](https://github.com/settings/tokens/new?scopes=repo&description=github-repos-dashboard)

- Select **Generate new token (classic)**
- Check the **`repo`** scope
- Copy the token immediately

### 4. Add the token as a secret

[![Add Secret](https://img.shields.io/badge/Add_Secret-yellow?style=for-the-badge)](https://github.com/HTL2910/github-repos-dashboard/settings/secrets/actions)

- Name: `PERSONAL_ACCESS_TOKEN`
- Paste your token as the value

### 5. Enable GitHub Pages

[![Open Pages Settings](https://img.shields.io/badge/Open_Pages_Settings-blue?style=for-the-badge)](https://github.com/HTL2910/github-repos-dashboard/settings/pages)

1. Source: **Deploy from a branch**
2. Branch: `main` / `/ (root)`
3. Click **Save**

Dashboard will be available at: [https://HTL2910.github.io/github-repos-dashboard/](https://HTL2910.github.io/github-repos-dashboard/)

### 6. (Optional) Add Contribution Snake

To show the animated contribution snake on your profile:

1. Go to your profile repo: [https://github.com/HTL2910/HTL2910](https://github.com/HTL2910/HTL2910)
2. Create file `.github/workflows/snake.yml` with this content:

```yaml
name: Generate Snake
on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:
jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: Platane/snk@v3
        with:
          github_user_name: HTL2910
          outputs: |
            dist/github-contribution-grid-snake.svg
            dist/github-contribution-grid-snake-dark.svg?palette=github-dark
      - uses: crazy-max/ghaction-github-pages@v4
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

3. Go to [Actions](https://github.com/HTL2910/HTL2910/actions) → run **Generate Snake**

### 7. Run the dashboard workflow

[![Run Workflow](https://img.shields.io/badge/Run_Workflow-success?style=for-the-badge)](https://github.com/HTL2910/github-repos-dashboard/actions/workflows/update-dashboard.yml)

This updates this README and your profile README.

### 8. View your profile

[![View Profile](https://img.shields.io/badge/View_Profile-blue?style=for-the-badge)](https://github.com/HTL2910/HTL2910)

---

**Web Dashboard**: [https://HTL2910.github.io/github-repos-dashboard/](https://HTL2910.github.io/github-repos-dashboard/)

**Updated**: 2026-11-10 04:43 UTC  
**Total**: 33 repos (0 private / 33 public)

---

## 🌐 Web / Frontend (4)

| Repo | Language | Updated | Stars | Visibility | Description |
|------|----------|---------|-------|------------|-------------|
| [github-repos-dashboard](https://github.com/HTL2910/github-repos-dashboard) | HTML | 2026-11-10 | 1 | 🌐 | Automated overview & manager for all personal GitHub reposit |
| [AWS-AI-chatbot](https://github.com/HTL2910/AWS-AI-chatbot) | TypeScript | 2026-11-04 | 0 | 🌐 |   SafeGraph AI - VS Code AI coding assistant with Amazon Bed |
| [bang-cards-deck](https://github.com/HTL2910/bang-cards-deck) | TypeScript | 2026-11-01 | 0 | 🌐 | - |
| [JavaScript-Project](https://github.com/HTL2910/JavaScript-Project) | HTML | 2025-02-17 | 0 | 🌐 | Learn JavaScript |

## 🎮 Unity / Game (19)

| Repo | Language | Updated | Stars | Visibility | Description |
|------|----------|---------|-------|------------|-------------|
| [Wocel](https://github.com/HTL2910/Wocel) | C# | 2026-10-08 | 0 | 🌐 | - |
| [Echo-of-the-Void](https://github.com/HTL2910/Echo-of-the-Void) | C# | 2026-09-26 | 0 | 🌐 | Echo of the Void là tựa game 2D Precision-Platformer kết hợp |
| [education](https://github.com/HTL2910/education) | C# | 2025-12-20 | 1 | 🌐 | unity 3d |
| [Environmental-Education](https://github.com/HTL2910/Environmental-Education) | C# | 2025-12-20 | 1 | 🌐 | Environmental Education Unity Game |
| [Farm](https://github.com/HTL2910/Farm) | C# | 2025-09-07 | 0 | 🌐 | Farming game made in Unity |
| [SaveDataUnity](https://github.com/HTL2910/SaveDataUnity) | ShaderLab | 2025-08-23 | 0 | 🌐 | Use Asset Bundles and addressable |
| [Voice_Game](https://github.com/HTL2910/Voice_Game) | C# | 2025-08-03 | 0 | 🌐 | use voice to play game |
| [photon_Game](https://github.com/HTL2910/photon_Game) | C# | 2025-08-03 | 0 | 🌐 | Photon Game Unity |
| [Whisper-For-Unity](https://github.com/HTL2910/Whisper-For-Unity) | - | 2025-07-22 | 0 | 🌐 | Use Whisper for Unity and select Model |
| [TestBuildingSystem](https://github.com/HTL2910/TestBuildingSystem) | C# | 2025-07-09 | 0 | 🌐 | testBuilding System - use System Surival  |
| [JellyField](https://github.com/HTL2910/JellyField) | ShaderLab | 2025-05-25 | 0 | 🌐 | unity clone test Jelly-Field |
| [Infinity-Ball](https://github.com/HTL2910/Infinity-Ball) | ShaderLab | 2025-05-17 | 0 | 🌐 | unity beginer |
| [URP_Game](https://github.com/HTL2910/URP_Game) | ShaderLab | 2024-12-15 | 0 | 🌐 | Use for URP Project Test |
| [Game-Developer-3D](https://github.com/HTL2910/Game-Developer-3D) | - | 2024-12-02 | 0 | 🌐 | Udemy Course |
| [Color-Maze-Adventure](https://github.com/HTL2910/Color-Maze-Adventure) | ShaderLab | 2024-11-20 | 0 | 🌐 | Unity Game Color Maze Adventure |
| [Game-Do_Vui](https://github.com/HTL2910/Game-Do_Vui) | ShaderLab | 2024-08-26 | 0 | 🌐 | unity game 2D |
| [UnityLearning](https://github.com/HTL2910/UnityLearning) | Mathematica | 2024-08-04 | 0 | 🌐 | https://learn.unity.com/ed-pd/course/teach-unity |
| [Casual-Game](https://github.com/HTL2910/Casual-Game) | ShaderLab | 2024-07-26 | 0 | 🌐 | unity |
| [BanMayBay2D](https://github.com/HTL2910/BanMayBay2D) | C# | 2024-03-17 | 0 | 🌐 | 2D unity Basic |

## 📁 Other (2)

| Repo | Language | Updated | Stars | Visibility | Description |
|------|----------|---------|-------|------------|-------------|
| [HTL2910](https://github.com/HTL2910/HTL2910) | - | 2026-11-10 | 0 | 🌐 | Config files for my GitHub profile. |
| [Power-BI](https://github.com/HTL2910/Power-BI) | - | 2024-08-21 | 0 | 🌐 | Hoc Power BI |

## 🤖 AI / ML (8)

| Repo | Language | Updated | Stars | Visibility | Description |
|------|----------|---------|-------|------------|-------------|
| [hypit](https://github.com/HTL2910/hypit) | - | 2026-10-05 | 0 | 🌐 | Clone any viral video with AI agents. Not just a script, the |
| [Full-Stack-Data-Science---Machine-Learning-BootCamp-Course](https://github.com/HTL2910/Full-Stack-Data-Science---Machine-Learning-BootCamp-Course) | Jupyter Notebook | 2026-09-25 | 0 | 🌐 | Learn Udemy Full Stack Data Science & Machine Learning BootC |
| [shorts](https://github.com/HTL2910/shorts) | Python | 2026-09-10 | 0 | 🌐 | 🎥 AI Youtube Shorts video generator using Gemini API for ima |
| [Interview-Project](https://github.com/HTL2910/Interview-Project) | Python | 2026-07-30 | 0 | 🌐 | Interview Job test |
| [Chay-Code](https://github.com/HTL2910/Chay-Code) | Python | 2025-08-29 | 0 | 🌐 | Chay code |
| [Web-Scraping_Web-Crawling](https://github.com/HTL2910/Web-Scraping_Web-Crawling) | Python | 2025-02-14 | 1 | 🌐 | Use Python 3, Selenium, BeautifulSoup and Chromium |
| [OpenCV-with-Python](https://github.com/HTL2910/OpenCV-with-Python) | Python | 2024-11-13 | 0 | 🌐 | OpenCV with Python:Recognition,Detection |
| [Graph-based-recommend-system-using-GNN](https://github.com/HTL2910/Graph-based-recommend-system-using-GNN) | Jupyter Notebook | 2024-07-26 | 0 | 🌐 | Đồ án tốt nghiệp |

---

*Generated automatically. Run the workflow to refresh.*