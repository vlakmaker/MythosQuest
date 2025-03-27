# 🔧 March 10 – Performance Tuning & Docker Pain

**Date:** 2025-03-10  
**Context:** Final week running MythosQuest using locally hosted models via Docker (Mistral/Gemma with Ollama)

---

## 🚧 Goal

Deploy MythosQuest on an Oracle ARM VM using Docker to self-host the AI Dungeon Master. This included:

- Running **Mistral** via Ollama
- Setting up **ChromaDB** for RAG support
- Hosting the app with **Flask** on port 5000
- Containerizing everything via **Docker Compose**

---

## 😤 What Went Wrong

| Issue | Description |
|------|-------------|
| 🐌 Slow response time | The self-hosted Mistral/Gemma models were **too heavy** for both local and cloud hardware. Each response took 1–3 minutes. |
| 💥 Docker build time | Image rebuilds could take **up to 5000+ seconds** due to complex dependencies (Chromadb, torch, transformers, etc). |
| 🧱 SQLite conflicts | Chroma required a specific `sqlite3` build which didn’t play nice with system Python or conda. |
| 🧵 Terminal vs Web | Performance was slightly better via terminal. The web UI using Flask with streaming was less optimized for full sentence chunks. |
| 💀 Oracle VM | The Oracle Ampere A1 (4 CPU, 24GB RAM) choked under the weight of even basic inference workloads. |

---

## 🔍 What We Tried

- Docker multistage builds ✅
- Reducing unused packages from requirements.txt ✅
- Switching to faster models (Gemma:2b instead of Mistral) ✅
- CPU offloading via Ollama ❌
- SQLite patching for Chroma ❌
- Running locally vs server-side 🧪

Despite our efforts, **hardware limitations were a consistent bottleneck**—especially with multi-user scalability in mind.

---

## 🔄 Decision: Switch to API-Based Inference

We paused all development on self-hosted inference and decided to:

✅ Use a **hosted LLM API (CosmosRP)** for gameplay  
✅ Park the **Docker-based branch** under `self-hosted-ai`  
✅ Create a new **fast API-powered branch (`main`)** for experimentation  

This gave us:

- Faster responses
- Lower maintenance overhead
- More time to focus on **game mechanics, memory, and narrative depth**

---

## 📎 Related Actions

- Created branches `self-hosted-ai` (Docker) and `main` (CosmosRP)
- Updated `.env` to use `COSMOSRP_API_KEY`
- Stripped unused Docker logic from main
- Started work on login system to restrict external access

---

## 🧩 Related Threads

- [March 22 – Switching to CosmosRP](./2025-03-22-api-switch.md)
- [March 27 – Login system plans](./2025-03-27-login-auth.md)

---
