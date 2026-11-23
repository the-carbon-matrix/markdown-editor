# Markdown Editor
A Simple Markdown Editor built using Flask and Vue.JS

# Features
1. **Admin Dashboard:** Allows admin to approve users, delete them, and preview their notes
2. **Editor Dashboard:** Allows editors to create and preview their notes

# Prerequisites
- Python 3.13
- Node v24.22.2
- Docker (Optional)

# Running the app
Copy `.env.example` to `.env` and set variables accordingly.

- `SECRET_KEY` can be generated via:
```sh
python -c "import secrets; print(secrets.token_urlsafe())"
```

- `SECURITY_PASSWORD_SALT` can be generated via:
```sh
python -c "import secrets; print(secrets.SystemRandom().getrandbits(128))"
```

## Via Docker Compose
```sh
sudo docker compose up --build -d
```

## Manually (without docker)
### 1. Frontend
```sh
cd ./frontend
npm ci
npm run dev
```

### 2. Backend
```sh
cd ./backend
uv sync
uv run python app.py
```

