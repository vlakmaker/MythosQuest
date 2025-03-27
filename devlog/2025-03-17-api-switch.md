# 🔁 March 17 – Switching to CosmosRP API

**Date:** 2025-03-17  
**Context:** MythosQuest had hit performance limits with self-hosted models (Ollama + Mistral/Gemma). This marked the transition to API-first development.

---

## 🚧 Why We Switched

| Problem | Impact |
|--------|--------|
| 🐌 Local inference was too slow | 2–5 min per reply on Oracle/PC |
| ⚙️ Docker builds were too large | Image builds took ~5000 seconds |
| 🧵 RAM/CPU bottlenecks | Oracle VM (24GB RAM, 4 ARM cores) couldn’t keep up |
| 🧱 Chroma + SQLite conflicts | Caused build failures and dev delays |
| 🔐 API security not enforced | Keys were vulnerable without login handling |

---

## ✅ Benefits of CosmosRP

| Benefit | Description |
|--------|-------------|
| 🚀 **Much faster responses** | < 10 seconds per call vs. 2+ minutes |
| ☁️ **No hosting burden** | Inference handled remotely — zero GPU needed |
| 📦 **Simplified requirements** | No Ollama, torch, transformers, etc. |
| 🛠️ **Faster iteration** | Less time debugging, more time building features |
| 🌍 **Scalability** | Prepares us for future multiplayer/shared use |

---

## 🔄 What Changed

- Replaced Ollama model call with `https://api.pawan.krd/cosmosrp-pro/v1/chat/completions`
- Introduced `.env` variable `COSMOSRP_API_KEY` to keep keys private
- Verified test connection via `test_cosmorp.py`
- Stripped out unnecessary dependencies (transformers, chromadb, etc.)
- Simplified Docker builds drastically
- Created fallback key rotation plan (for public testing)

---

## 📁 Code Updates

| File | Change |
|------|--------|
| `ai_dm.py` | Switched `ollama.chat` to `requests.post()` for CosmosRP |
| `.env` | Added `COSMOSRP_API_KEY=...` |
| `requirements.txt` | Removed heavy packages, added `python-dotenv`, `requests` |
| `test_cosmorp.py` | Standalone script to verify API call success |

---

## 🌱 What's Next

- Add login system to protect API usage
- Monitor CosmosRP token usage and pricing
- Add retry handler for CosmosRP API downtime
- Improve prompt structure for RP output consistency

---

## 📎 Related Devlogs

- [March 10 – Performance tuning & Docker pain](./2025-03-10-performance-tuning.md)
- [March 27 – MythosQuest goes live](./2025-03-27-cosmosrp-launch.md)
- [March 27 – Login system plans](./2025-03-27-login-auth.md)

---

> MythosQuest took its first step from hobby to scalable app with this change. 🚀
