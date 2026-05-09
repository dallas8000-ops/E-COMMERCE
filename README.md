# Kistie-Store

[![CI](https://github.com/dallas8000-ops/Kistie-Store/actions/workflows/ci.yml/badge.svg)](https://github.com/dallas8000-ops/Kistie-Store/actions/workflows/ci.yml)

Live **fashion ecommerce** (women’s apparel & accessories)—shipping from **Kampala**, serving customers online worldwide. Production **Django** storefront + staff tooling + **DRF** API on **Render** / **PostgreSQL**, **tests + CI** on every push to `main`.

| | |
|--|--|
| **Live** | https://kristie-store.onrender.com |
| **Code** | https://github.com/dallas8000-ops/Kistie-Store |
| **Trello** | https://trello.com/b/s8Rpm9in/kistie-store |
| **Planning** | [PROJECT_PLANNING.md](PROJECT_PLANNING.md) |

---

## What it does (short)

**Shoppers:** catalog (filters, reviews), inventory (EU sizes, multi-currency), cart, checkout with live FX, auth, contact. **Payments** are confirmed by staff in the real world, then order status is updated in **Django admin** (typical for boutique + East Africa payment mix).

**Operations:** custom-theme **Django admin**, **staff dashboard** (`/staff/dashboard/`), **audit log** for superusers, CSRF + login throttling, **public read / staff-only write** on inventory API.

**Why this stack:** Django **SSR** for the live path (SEO, sessions, security); **React + Vite** in `frontend/` for future pages; DRF already exposes JSON for that migration.

---

## Pages & Features

| Page | URL | What it does |
|------|-----|--------------|
| Home | `/` | Brand landing, hero section |
| About | `/about/` | Brand story and market context |
| Catalog | `/catalog/` | Database-backed product grid with detail modal |
| Inventory | `/inventory/` | EU sizes, quantity, currency & payment method selectors |
| Cart | `/cart/` | Line items, server-side totals, currency conversion |
| Checkout | `/checkout/` | Order capture, payment instructions, order reference |
| Auth | `/signup/` `/login/` `/logout/` | Shopper accounts; guest cart merges on login |
| Staff sign in | `/staff/login/` | Dedicated entry for portal staff → redirects to staff dashboard |
| Contact | `/contact/` | Inquiry form → admin persistence + SMTP email |
| Terms | `/terms/` | Terms of Service |
| Staff Dashboard | `/staff/dashboard/` | Orders snapshot, low-stock alerts, recent inquiries (permission-gated) |
| Order history | `/account/orders/` | Signed-in shopper order list |
| Admin | `/admin/` | Full Django admin: products, images, orders, users (superusers) |
| Health | `/health/` | Uptime monitor endpoint → `{"status":"ok"}` |
| API | `/api/` | DRF JSON API (public read / staff write) |

---

## Tech (recruiter lines)

Python · **Django** · **Django REST Framework** · **PostgreSQL** (prod) / SQLite (dev) · Gunicorn · WhiteNoise · **Render** · **GitHub Actions** · Bootstrap 5 · **Bootstrap Icons** · custom CSS (gradients + branded buttons) · Pillow

---

## Proof — screenshots

**In-repo gallery:** everything under [`images/screenshots/`](images/screenshots/) (storefront, brand shots, full **admin** set: login, dashboard, products, users, groups, carts, reviews, inquiries). The same images are **embedded in the capstone submission document** (PDF/report) for reviewers who use that packet.

**Highlights:**

| Storefront | Admin |
|------------|--------|
| ![Catalog](images/screenshots/Catalog.png) | ![Admin hub](images/screenshots/admin-dashboard.png) |

![Products in admin](images/screenshots/admin-products.png)

**Auto-play slide deck** (storefront + admin + API summary): open [`docs/demo-presentation.html`](docs/demo-presentation.html) after `python -m http.server 8080` from repo root → `http://127.0.0.1:8080/docs/demo-presentation.html` (or use [ScreenToGif](https://www.screentogif.com/) to record a short GIF for LinkedIn).

---

## Reviewer / demo access (capstone)

- **Live site:** same URL as in the table above (`/`, `/inventory/`, `/staff/login/`, etc.).
- **Django admin:** `/admin/` — **demo username and password** are provided in the **official submitted capstone package** (not duplicated in this public README).
- **No packet?** Email [dallas8000@gmail.com](mailto:dallas8000@gmail.com).

---

## Run locally

```bash
cd backend
cp .env.example .env   # set DJANGO_SECRET_KEY
python manage.py migrate
python manage.py runserver
# http://127.0.0.1:8000/  —  createsuperuser for /admin/
```

Optional: `frontend/` and `payments/` for React/Node experiments. `render.yaml` documents production service shape.

---

## Production hardening

When **`DEBUG=False`** (Render): **HTTPS proxy headers** respected (`X-Forwarded-Proto`), **secure session + CSRF cookies**, **SSL redirect**, **`X-Frame-Options: DENY`**, structured **logging** to stdout (level via `DJANGO_LOG_LEVEL`). Optional **HSTS**: set `DJANGO_HSTS_SECONDS` (e.g. `31536000`), optionally `DJANGO_HSTS_INCLUDE_SUBDOMAINS`, `DJANGO_HSTS_PRELOAD`. **Dev CORS** for Vite runs **only when `DEBUG=True`**.

**Health checks:** `GET https://kristie-store.onrender.com/health/?format=json` → `{"status":"ok","service":"kistie-store"}` for uptime monitors.

---

## CI

[`.github/workflows/ci.yml`](.github/workflows/ci.yml) — `pip install -r requirements.txt` then `cd backend && python manage.py test` on **push/PR** to `main` or `master`.

---

## Contact

**Barney R. Gilliom** — built and runs this stack for **Kistie-Store** as a live retail business.

dallas8000@gmail.com · [LinkedIn](https://www.linkedin.com/in/barney-gilliom-959981337) · [GitHub](https://github.com/dallas8000-ops) · [Portfolio](https://jnalumansi.onrender.com)

Business questions: use the **live site** contact or the email above.
