# 🧙 MythosQuest Devlog – Week of April 22, 2025

This week marked a huge milestone in MythosQuest's evolution — we reached a stable MVP with full user login, secure API key storage, and dynamic gameplay settings!

## ✅ Highlights

### 🔐 Secure API Key Management
- Implemented **Fernet encryption** for storing API keys securely in the database
- Moved encryption key to `.env` for safe access
- Created `/api/keys` routes to **save and fetch provider-specific API keys**
- Keys are masked in the frontend and decrypted only when streaming a prompt

### 🛠️ Database & ORM Refactor
- Replaced raw SQLite access with **full SQLAlchemy ORM** for both:
  - `User` model (login, settings)
  - `APIKey` model (per-provider, per-user)
- Database schema now includes:
  - `selected_model`
  - `context_size`
  - `api_url` for each provider
- Improved `get_current_user()` and `get_user_api_key()` for ORM compatibility

### 🖥️ Frontend Settings Page Overhaul
- Rebuilt settings UI into **two clean sections**:
  1. **Gameplay Settings** (provider, temperature, context size)
  2. **Secure API Key Storage** per provider
- Each provider section includes:
  - Masked API key input
  - Custom API URL input
  - Individual save buttons
- JS dynamically loads/saves settings via `fetch()`

### 📡 Streaming Logic & Config Integration
- Updated `stream_response()` to:
  - Dynamically pull provider, key, URL, model, and context size per user
  - Support both OpenRouter and Cosmos APIs with modular logic
  - Yield streamed responses in real time without breaking session context

### 🐛 Bug Fixes & Cleanup
- Fixed circular imports by reorganizing `load_settings()`
- Resolved multiple `RuntimeError: Working outside of request context` issues
- Ensured consistent behavior on login/logout
- Polished layout and spacing for a more cohesive UI

## 🧭 Next Steps

### 🔜 CI/CD Pipeline (Phase 9)
- Dockerize MythosQuest backend for consistent deployment
- Add GitHub Actions for:
  - ✅ Testing with `pytest`
  - ✅ Code quality checks
  - 🚀 Automatic deployment to staging/production
- Choose initial deployment target (Fly.io, Oracle Cloud, etc.)

### 🧪 In Progress
- Model dropdown per provider (auto-populated + custom option)
- Finalize context size integration
- UI polish + mobile friendliness

---

_This was a breakthrough week. We're now entering the infrastructure and polish stage. Time to bring MythosQuest to life beyond localhost!_

🛠️ Built with Flask, SQLite, SQLAlchemy, Fernet, and ✨ determination.
