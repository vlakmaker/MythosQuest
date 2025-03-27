# 🧙 MythosQuest Dev Log – Login System & User Authentication

**Date:** 2025-03-27  
**Author:** vlakmaker  
**Context:** Phase 2 – Enabling private access and session support.

---

## ✨ Summary

To prepare MythosQuest for eventual online deployment while keeping access limited, we’re building a **simple but secure login system** using:

- Flask’s built-in session management
- Flask-Login for authentication
- SQLite for local user storage
- Password hashing via `werkzeug.security`

This system will allow individual users to log in and eventually return to their sessions. We’ll scaffold user registration, login, and logout with templates, and ensure that no passwords are stored in plaintext.

---

## ✅ Objectives

- [ ] Require login to access the game
- [ ] Store user credentials securely in SQLite
- [ ] Build basic login + logout pages
- [ ] Optional: Add registration form
- [ ] Add user session loading for memory recall (planned)

---

## 🔒 Design Decisions

- **Flask-Login**: Handles session tracking and access control.
- **SQLite**: Easy, portable, and sufficient for this phase.
- **Hashed Passwords**: Using `werkzeug.security.generate_password_hash` and `check_password_hash`.
- **No plaintext storage**: Passwords will *never* be logged, saved, or sent over the wire unencrypted.
- **Static user admin** will be replaced by registration and admin tools later.

---

## ❓ FAQ

### Why not use a cloud database?
> MythosQuest is still an experimental solo project. SQLite is lightweight and keeps everything self-contained. We’ll evaluate cloud options once multiplayer and persistence features are needed.

### Can I reset or change passwords?
> Not yet. We’re starting with static login credentials. Password reset flows are a later enhancement.

### Can you see my password?
> **No.** All passwords are hashed using strong one-way encryption. Even the developer cannot see your real password.

### Is registration open to anyone?
> Right now, logins are local and controlled manually. We’ll explore private invites or token-based access if MythosQuest becomes multi-user.

---

## 🔧 Upcoming

- Add `/register` route for new users
- Enable user-specific memory logs
- Protect memory access on a per-session basis
- Add basic role management (e.g. admin/player)

---

## 🧩 Related Threads

- [March 26 – Switching from Ollama to CosmosRP](./2025-03-26-api-switch.md)
- [March 10 – Performance tuning & Docker pain](./2025-03-22-api-switch.md)

---

