# 🛤️ MythosQuest – Product Roadmap

This document outlines the staged development of MythosQuest — an immersive, AI-powered storytelling platform focused on historically guided roleplay. Each phase builds toward a stable, creative, and inspiring user experience rooted in history, exploration, and narrative depth.

---

## 🧭 1. Vision Statement

**MythosQuest** is the only AI storytelling platform that combines guided roleplay with immersive, historically accurate scenarios — designed for both casual story lovers and dedicated worldbuilders.

---

## 🚀 2. Phase Overview

| Phase | Goal | Status |
|-------|------|--------|
| Phase 0 | Experiment with Ollama + local models | ✅ Completed |
| Phase 1 | Switch to CosmosRP API, create minimal web app | ✅ Completed |
| Phase 2 | Add login & registration (Flask + SQLite) | ✅ Completed |
| Phase 3 | Polish frontend + streaming fixes | ✅ In Progress |
| Phase 4 | Design scenario engine + character creation | 🔜 Planned |
| Phase 5 | Session memory per user (last 5 turns) | 🔜 Planned |
| Phase 6 | Historical scenario templates | 🔜 Planned |
| Phase 7 | Lore engine, skill modifiers & event logic | 🔜 Backlog |
| Phase 8 | Refactor to clean app structure | 🔜 Backlog |
| Phase 9 | Docker CI/CD + production-ready deployment | 🔜 Backlog |
| Phase 10 | Community access, feedback, & private testing | 🔜 Later

---

## 🎯 3. MVP Feature Checklist

| Feature | Description | Status |
|--------|-------------|--------|
| ✅ Login system | Flask + SQLite with session management | ✅ Done |
| ✅ CosmosRP API integration | Streaming AI responses | ✅ Done |
| ✅ Basic UI | Web interface with prompt input + response | ✅ Done |
| ⬜ Character creator | Name, origin, 2–3 skills | 🔜 Planned |
| ⬜ Scenario selector | Rome, French Revolution, more | 🔜 Planned |
| ⬜ Prompt builder | Custom templates using scenario + skills | 🔜 Planned |
| ⬜ Response streamer | With buffer logic + delayed updates | ✅ Partial |
| ⬜ Session memory | Per user, stores last 5 turns | 🔜 Planned |
| ⬜ Lore templates | Prewritten scenario hooks + setting | 🔜 Backlog |

---

## 💎 4. Unique Value

Unlike JanitorAI or AI Dungeon, **MythosQuest** sits in the middle:

- More structure than chatting with a random character
- Less complex than a full RPG battle system
- Focuses on **immersive, historical storytelling** — not fantasy combat
- Encourages **curiosity, agency, and reflection**

---

## 🧪 5. Success Signals

These early metrics will guide iteration:

- ✅ **“Did I enjoy playing it myself?”**
- 🧠 “Did it help me create a scene or idea I wouldn’t have thought of alone?”
- 💬 “Do users say it feels more guided or immersive than other chat AI tools?”
- 💡 “Did someone want to *come back* and play again?”

---

## 🧱 6. Next Steps

- [ ] **Refactor core app** into cleaner structure (`/routes`, `/models`, `/templates`)
- [ ] Improve session handling and route protection
- [ ] Finalize character + scenario flow
- [ ] Store last 5 user turns per session
- [ ] Build basic lore scenario picker (HTML or dropdown)

---

## 🗺️ 7. Long-Term Dreams

- Richer scenario builder for advanced users
- Skill-based event randomness + stat growth
- “History mode” with real-world facts woven in
- Cross-player timelines or alternate histories
- Private or public campaign sharing

---

**Last updated:** 2025-04-15

