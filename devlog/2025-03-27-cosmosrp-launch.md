# 🚀 March 27 – MythosQuest Launches with CosmosRP

**Date:** 2025-03-27  
**Milestone:** MythosQuest officially live and publicly accessible via Oracle Cloud (secured via API key rotation)  
**Focus:** Performance, simplification, API transition

---

## 🎉 Summary

After weeks of iteration, testing, and Docker wrangling, **MythosQuest** is now live on my Oracle Cloud instance — powered by the **CosmosRP API** instead of local models like Mistral or Gemma.

This shift marks a major milestone in the project:  
> **From self-hosted hobbyist prototype ➝ toward a fast, scalable, narrative AI engine.**

---

## 🔄 Key Changes Made Today

| Area             | Description |
|------------------|-------------|
| 🧠 AI Model       | Replaced local Ollama/Mistral with the much faster `cosmosrp-pro` API |
| 🧼 Code Cleanup   | Removed login, memory, and RAG features from `ai_dm.py` to keep the system simple and focused |
| 🔑 Secrets        | Switched to `.env`-based API key handling using `python-dotenv` for better security |
| 🐳 Docker         | Verified new version works both locally and via Docker on the Oracle server |
| 🔐 Temporary Security | API key rotated to prevent external access until login protection is implemented |

---

## 🌍 Deployment Status

- ✅ Running locally on `localhost:5000`
- ✅ Running via Docker container on Oracle Cloud VM (AMPERE A1 - ARM 4 CPU, 24 GB RAM)
- ✅ Verified with `curl` and browser
- 🔒 Secured from public use by disabling the production API key

---

## 🤯 What We Learned

| Realization | Impact |
|-------------|--------|
| CosmosRP is **WAY faster** than local Ollama models | Drastically improves perceived performance |
| Simpler is better when iterating | Removing unneeded features made testing and debugging a breeze |
| `.env` management matters | One misplaced key can leak credentials – but was quickly resolved with `git filter-repo` |
| Docker + CosmosRP is a powerful combo | Especially when hardware is limited, APIs scale better |

---

## 🛣️ Next Steps

- 🧪 Build a simple login system to restrict access
- 🔐 Secure API usage before re-enabling external access
- 🗂️ Improve file and folder structure (separate modules, templates, static assets)
- 🧠 Reintroduce memory + context once speed + UX are solid
- 🎨 Update UI for a more immersive experience

---

## 📎 Related Devlogs

- [March 10 – Performance tuning & Docker pain](./2025-03-10-performance-tuning.md)
- [March 22 – Switching to CosmosRP](./2025-03-17-api-switch.md)
- [March 27 – Login system plans](./2025-03-27-login-auth.md)

---

## ✅ Committed Under

Branch: `main`  
Commit: _(replace with your commit hash)_  
Repo: [MythosQuest](https://github.com/vlakmaker/MythosQuest)

---

## 💬 FAQ

**Q: Why switch from Mistral/Gemma to CosmosRP?**  
A: Running inference locally was far too slow (up to 5 minutes per reply). CosmosRP gave us immediate speed boosts and flexibility.

**Q: Why remove memory/login/RAG?**  
A: Simpler debugging. Now that the core system works, we'll reintroduce those in later milestones.

**Q: Is this production-ready?**  
A: Not yet! It's a working prototype. Security, scalability, and UX will come next.

---

> MythosQuest started as an experiment in AI storytelling. It’s now a living project — and today, it became real.
