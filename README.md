# Kistie-Store

[![CI](https://github.com/dallas8000-ops/Kistie-Store/actions/workflows/ci.yml/badge.svg)](https://github.com/dallas8000-ops/Kistie-Store/actions/workflows/ci.yml)

**Kistie-Store** is her retail brand—a live **fashion ecommerce** business focused on women’s apparel and accessories, serving customers with shipping from **Kampala, Uganda**, and a worldwide audience online. This repository is the **production codebase** I built and operate for that business: a Django-backed storefront, staff tooling, and a secured REST API—**deployed on Render** with **PostgreSQL**, with **automated tests on every push** via GitHub Actions.

**Live site:** https://kistie-store.onrender.com  
**Source:** https://github.com/dallas8000-ops/Kistie-Store

---

## Overview

The customer journey runs on **server-rendered Django templates**: home, **catalog** (filters, reviews), **inventory** (EU sizes, multi-currency), **cart**, **checkout**, authentication, and **contact**. Orders are placed in the system; **payment is confirmed by staff** after real-world verification (mobile money, bank, WorldRemit, etc.)—a common model for boutique retail and strong fit for East African payment habits—then status is updated in **Django admin**.

Operations extend beyond the default admin: **staff** get a **dashboard** (orders, revenue by currency, low stock, inquiries); **superusers** can review an **audit trail** of admin actions. The UI is **responsive**, supports **light/dark theming**, and uses **custom branding** (including an optional styled Django admin).

---

## What I engineered (recruiter snapshot)

| Area | Implementation |
|------|------------------|
| **Storefront** | Django 5, SSR, Bootstrap 5, session + user carts, merge on login, stock checks |
| **Money** | Live FX via Frankfurter API with fallbacks; checkout in USD/EUR/KES/UGX |
| **API** | Django REST Framework — **public read** on products/categories; **writes restricted to staff**; throttling |
| **Quality** | Automated test suite + **CI on `main`** |
| **Hosting** | Gunicorn, WhiteNoise, **PostgreSQL** on Render (`render.yaml`), health endpoint |

---

## Tech stack

- **Backend:** Python, Django, Django REST Framework, Gunicorn  
- **Database:** SQLite (local); **PostgreSQL** in production (`dj-database-url`)  
- **Frontend (live path):** Django templates, Bootstrap 5, custom CSS  
- **Future / parallel:** React 19 + Vite (`frontend/`), Node stubs (`payments/`) for optional gateway experiments  
- **Infra:** Render, GitHub Actions CI  

---

## Features

### Storefront & discovery
- Home with featured products and category entry points  
- **Catalog** — filters (category, USD band, EU size), product imagery, moderated **review averages** on cards  
- **Inventory** — sizing, quantity, currency preference, add to cart  
- **About** & **contact** — inquiries stored and emailed (SMTP configurable)  
- **Theming** — dark/light + palette options  

### Cart, checkout & orders
- Guest and authenticated carts; merge when signing in  
- Checkout with live rates and order reference  
- **Order history** for signed-in customers  

### Staff & back office
- **Django admin** — products, categories, images, orders, inquiries, reviews (when admin URL enabled on hosting)  
- **Staff dashboard** (`/staff/dashboard/`)  
- **Audit log** (`/staff/audit-log/`) for superusers  
- Custom admin presentation (`kistie_admin.css`, `base_site.html`)  

### API & security
- `GET /api/inventory/categories/`, `GET /api/inventory/products/` — public, throttled  
- Mutating requests — **`is_staff` required**  
- CSRF on HTML forms; configurable trusted origins; login attempt throttling  

---

## Architecture

The **live storefront** is intentionally **Django SSR** for speed to market, SEO-friendly pages, and built-in CSRF/session security without shipping a JS bundle for the critical path.

**React + Vite** exists as a **separate workspace** for future high-interactivity screens; the DRF layer already supports a gradual move (public reads today, staff-only writes).

---

## Screenshots

Assets live in `images/screenshots/`:

| Area | File |
|------|------|
| **Storefront** — catalog & inventory | [`Catalog.png`](images/screenshots/Catalog.png) |
| **Brand** — Kampala / location imagery | [`Central Kampala.png`](images/screenshots/Central%20Kampala.png), [`Downtown Night.png`](images/screenshots/Downtown%20Night.png), [`Pearl of Africa.png`](images/screenshots/Pearl%20of%20Africa.png) |
| **Admin** — dashboard (hub) | [`admin-dashboard.png`](images/screenshots/admin-dashboard.png) |
| **Admin** — products (USD + UGX, filters) | [`admin-products.png`](images/screenshots/admin-products.png) |
| **Admin** — login | [`admin-login.png`](images/screenshots/admin-login.png) |
| **Admin** — users | [`admin-users.png`](images/screenshots/admin-users.png) |
| **Admin** — groups | [`admin-groups.png`](images/screenshots/admin-groups.png) |
| **Admin** — carts | [`admin-carts.png`](images/screenshots/admin-carts.png) |
| **Admin** — product reviews | [`admin-product-reviews.png`](images/screenshots/admin-product-reviews.png) |
| **Admin** — contact inquiries | [`admin-contact-inquiries.png`](images/screenshots/admin-contact-inquiries.png) |

### Storefront — catalog & inventory

![Catalog and inventory](images/screenshots/Catalog.png)

### Django admin — operations

Custom dark-theme Django admin (`kistie_admin.css`): store hub, catalog, orders, and leads.

![Admin — store operations hub](images/screenshots/admin-dashboard.png)

![Admin — products](images/screenshots/admin-products.png)

### Brand imagery

![Central Kampala](images/screenshots/Central%20Kampala.png)

![Downtown Night](images/screenshots/Downtown%20Night.png)

![Pearl of Africa](images/screenshots/Pearl%20of%20Africa.png)

### Quick demo deck (auto-play slides)

**No login required** to run the deck—it is a static HTML file. To make **images load reliably**, serve the repo root with Python, then open the deck in the browser:

```bash
# From the kistie-store folder (repo root, where README.md lives):
cd path/to/kistie-store
python -m http.server 8080
```

Then visit: **http://127.0.0.1:8080/docs/demo-presentation.html**

The deck **auto-advances ~5.5s**; use **← / → / Space** and **Pause** in the bar. Slides include **storefront**, **Django admin dashboard**, **products**, plus API and live URL.

See [`docs/demo-presentation.html`](docs/demo-presentation.html).

**Record a GIF for LinkedIn or your portfolio:** use [ScreenToGif](https://www.screentogif.com/) (Windows) or **OBS** → export as video → convert to GIF, or share the **MP4** directly on LinkedIn. Full-screen the deck, hit **Play**, and record 20–30 seconds.

---

## Deployment (Render)

- **Web service:** Python, Oregon (see your Render dashboard)  
- **Database:** PostgreSQL (linked via `DATABASE_URL`)  
- Production **admin URL** can be toggled with `DJANGO_ENABLE_ADMIN` per `render.yaml` / dashboard env  
- **Media:** uploaded files live on instance disk; for heavy catalog growth, plan **persistent disk** or **object storage**  

---

## Continuous integration

[`.github/workflows/ci.yml`](.github/workflows/ci.yml) installs dependencies from `requirements.txt` and runs:

```bash
cd backend && python manage.py test
```

on pushes and pull requests to **`main`** or **`master`**.

---

## Local development

1. **Backend**
   ```bash
   cd backend
   cp .env.example .env   # if present; set DJANGO_SECRET_KEY
   python manage.py migrate
   python manage.py runserver
   ```
2. **Optional:** seed/link images per existing management commands (`seed_inventory_if_empty`, `link_static_images_to_products`) if you use the `images/` workspace folder.  
3. **React / payments** — see `frontend/` and `payments/` for `npm install` and dev servers (optional for the main Django storefront).

**Superuser (local admin):** `python manage.py createsuperuser` → `http://127.0.0.1:8000/admin/`

---

## Repository layout

| Path | Role |
|------|------|
| `backend/` | Django project, templates, apps (`core`, `inventory`, `cart`, `pages`) |
| `frontend/` | React + Vite (expansion) |
| `payments/` | Node stubs for future payment integrations |
| `images/` | Screenshots and optional seed imagery |
| `render.yaml` | Render service blueprint |

---

## Roadmap (product & engineering)

- Optional **automated payment webhooks** when a provider is chosen  
- **Durable media** (S3-compatible or Render disk) at higher catalog volume  
- Richer **order history** and optional **public review submission** (reviews today are staff-moderated)  
- Stricter **`SECURE_*` cookie settings** when using a custom domain with HTTPS end-to-end  
- Optional **django-ratelimit** / **django-axes** for additional abuse protection  

---

## Engineering milestones (recent)

- Staff-only **writes** on inventory API + DRF throttles  
- **GitHub Actions** CI on every push to `main`  
- Authentication, cart merge, contact notifications, staff dashboard, audit views  
- Responsive storefront verified on phone and tablet  

---

## About the platform engineer

**Barney R. Gilliom** — full-stack engineer; designed and built this stack to support **Kistie-Store** as an operating retail business (catalog, orders, staff workflows, cloud deployment).

**Stack focus:** Python · Django · Django REST Framework · PostgreSQL · React · Node.js · cloud deployment (Render) · CI/CD (GitHub Actions)

**Contact:** dallas8000@gmail.com · [LinkedIn](https://www.linkedin.com/in/barney-gilliom-959981337) · [GitHub](https://github.com/dallas8000-ops) · [Portfolio](https://jnalumansi.onrender.com)

For **business or partnership** questions about **Kistie-Store**, use the contact channels on the live site or the email above.
