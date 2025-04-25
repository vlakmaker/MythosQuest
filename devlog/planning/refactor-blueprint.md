/mythosquest
├── app/
│   ├── routes/
│   │   ├── auth_routes.py       # login, logout, register
│   │   └── game_routes.py       # homepage, generate
│   ├── templates/               # login.html, register.html, index.html
│   ├── static/                  # for CSS/JS later
│   ├── ai.py                    # stream_response()
│   ├── auth.py                  # session helpers (optional for later)
│   ├── models.py                # get_user, add_user (already good)
│   └── __init__.py              # app + blueprint init
├── config.py                    # environment loading + config
├── run.py                       # single entry point
├── requirements.txt
├── .env
