# Comments — SPA

A single-page **comments** application. Users leave comments (name, e-mail, optional
home page, image captcha, HTML-limited text); replies cascade to unlimited depth; root
comments show in a sortable, paginated table; files can be attached; and new comments
appear live over WebSocket.

## Features

- **Comment form** — User Name (Latin letters + digits), E-mail, Home page (optional URL),
  image **CAPTCHA**, and Text limited to the allowed HTML tags.
- **Cascading replies** — unlimited depth.
- **Sortable root table** — sort by User Name / E-mail / date (asc + desc), paginated
  **25 per page**, default order LIFO.
- **Allowed HTML only** — `a`, `code`, `i`, `strong`; XHTML tag-closing validation;
  protection against XSS and SQL injection.
- **Attachments** — image (JPG/GIF/PNG, auto-resized to ≤ 320×240) or `.txt` (≤ 100 KB),
  shown in a lightbox viewer.
- **AJAX preview** without page reload, HTML toolbar `[i] [strong] [code] [a]`.
- **Client + server validation**.
- **Live updates** over WebSocket.
- **JWT auth** (optional register / login), background queue (Celery), cache (Redis).

## Stack

- **Backend:** Django + DRF, Channels on Uvicorn (ASGI), Celery, Redis, MySQL 8,
  SimpleJWT, nh3, lxml, Pillow, django-tree-queries.
- **Frontend:** Vue 3 + Vite, Pinia, Vue Router, Axios.
- **Infra:** Docker Compose, nginx.

## Requirements

- Docker + Docker Compose.
- For local frontend dev: Node 20+.

## Setup

```bash
git clone <repo-url>
cd dzencode-comments
cp .env.example .env
# edit .env: set SECRET_KEY and the DB passwords
```

## Run — development

```bash
docker compose up -d --build                 # backend (Django/uvicorn) on :8000
cd client && npm install && npm run dev       # frontend (Vite) on :5173
```

Open http://localhost:5173. The Vite dev server proxies `/api`, `/ws`, `/media` to `:8000`.

Create an admin user:

```bash
docker compose exec web python manage.py createsuperuser
```

## Run — production (local)

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

Open http://localhost/. nginx serves the built SPA and proxies `/api`, `/ws`, `/media`,
`/static`; the backend runs under uvicorn with `config.settings.prod`.

## Deploy on a VDS (Hetzner)

1. Create an Ubuntu server, add your SSH key, note the public IP.
2. SSH in and install Docker:
   ```bash
   curl -fsSL https://get.docker.com | sh
   ```
3. Clone the repo and prepare env:
   ```bash
   git clone <repo-url> && cd dzencode-comments
   cp .env.example .env
   # in .env: add the server IP to DJANGO_ALLOWED_HOSTS,
   # set CSRF_TRUSTED_ORIGINS=http://<server-ip>, and use strong secrets
   ```
4. Start the stack and open port 80:
   ```bash
   docker compose -f docker-compose.prod.yml up -d --build
   ufw allow 80          # or open port 80 in the Hetzner firewall
   ```
5. Visit `http://<server-ip>/`.

## Database schema

`docs/schema.sql` — open in **MySQL Workbench** (*File → Open SQL Script*, or *New Model →
File → Import → Reverse Engineer MySQL Create Script* for the EER diagram).
