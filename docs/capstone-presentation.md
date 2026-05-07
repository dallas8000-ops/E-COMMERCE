# Kistie Store — Capstone Presentation Guide

## Elevator Pitch (30 seconds)

> "Kistie Store is a full-stack e-commerce web application for a women's fashion boutique based in Kampala, Uganda. It lets customers browse premium imported fashion curated from Turkey, UK, and USA, add items to cart, and complete orders via WhatsApp or online payment. Store managers get a full inventory management system with real-time stock tracking, bulk import/export, and an admin dashboard — all deployed on Render with a PostgreSQL production database."

---

## Demo Walkthrough (8–10 minutes)

### 1. Home Page — `/` (60 sec)
**Show:** Branded hero, Shop by Style tiles, New In featured products.  
**Say:**
- The hero dynamically pulls live stats (item count, collections) from the database.
- "Order on WhatsApp" button opens a pre-filled WhatsApp message — zero friction for mobile customers in East Africa.
- Dark mode toggle in the navbar persists across pages.
- All product cards show EU sizing badges because the target market sources from European fashion suppliers.

### 2. Catalog / Shop — `/catalog/` (60 sec)
**Show:** Filter bar (category, size, price, search), product grid, add to cart.  
**Say:**
- Filters are applied server-side via Django query params — fast and SEO-friendly.
- Each product card shows live stock count and EU sizes.
- "Add to Cart" uses Django sessions — works without login.

### 3. Cart — `/cart/` (45 sec)
**Show:** Cart table, quantity adjust, remove item, order total.  
**Say:**
- Cart is session-based so customers don't need an account to shop.
- The table is fully responsive — collapses cleanly on mobile.
- "Proceed to Checkout" leads to the payment flow.

### 4. Authentication — `/signup/`, `/login/`, `/logout/` (45 sec)
**Show:** Sign up form, customer sign-in, sign out; optional **Staff sign in** at `/staff/login/` (portal users land on `/staff/dashboard/`).  
**Say:**
- Storefront uses Django’s session auth; guest carts merge when a shopper logs in.
- **Staff dashboard** uses a custom permission (`access_staff_dashboard`); superusers can still open everything.
- Passwords are hashed with Django’s default PBKDF2/SHA256.

### 4b. Terms of Service — `/terms/` (15 sec)
**Show:** Legal / policy copy for the storefront.  
**Say:** Published Terms page for capstone and real-customer readiness.

### 5. About Page — `/about/` (30 sec)
**Show:** Brand story, team photo area, trust badges.  
**Say:**
- Static content page that reinforces brand identity and builds customer trust.
- Kampala-specific context: delivery partners (MTN, Airtel, WorldRemit), EU sizing guide.

### 6. Contact — `/contact/` (30 sec)
**Show:** Contact form, WhatsApp CTA, social links.  
**Say:**
- Form submissions are stored in the database and visible in the admin panel.
- Admin can review all customer enquiries from the Django admin.

### 7. Shop / Inventory — `/inventory/` (primary catalog) (90 sec)
**Show:** Product grid with EU sizes, filters, currency, add to cart; `/catalog/` redirects here.  
**Say:**
- Main shopping UX is server-rendered Django; inventory API backs data and staff workflows.
- Stock and product edits for production happen in **Django admin** (and staff dashboard for snapshots); CSV flows may live in admin or API depending on deployment.

### 8. Django Admin Panel — `/admin/` (superuser) (60 sec)
**Show:** Dashboard, Products, Cart sessions, Contact Inquiries, Users, Groups.  
**Say:**
- Standard Django admin extended with custom list displays and filters.
- Portal-only staff use `/staff/login/` and **do not** rely on Django admin; superusers manage users and assign the staff-dashboard permission.
- Contact inquiries and orders are reviewable here for operations.

### 9. Responsive Design — Quick demo (30 sec)
**Show:** Resize browser or open DevTools mobile view on Home or Catalog.  
**Say:**
- Bootstrap 5.3.2 grid + custom `brand.css` breakpoints at 768px and 576px.
- Navbar collapses to hamburger, hero stats stack to single column, catalog goes 1-up on mobile.
- Designed mobile-first because the primary customers are smartphone users in Uganda.

---

## Talking Points

### What's Implemented ✅
| Area | Details |
|------|---------|
| **Full-stack Django app** | Models, views, templates, URL routing, Django ORM |
| **Product catalog** | Category + size + price + keyword filtering, pagination |
| **Session-based cart** | Add/remove/update quantities, order total calculation |
| **Inventory management** | CRUD, CSV import/export, image upload, stock tracking |
| **Authentication** | Signup, login, logout, permission-gated views |
| **Contact form** | Form validation, DB storage, admin review |
| **Dark mode** | JS toggle, persisted via localStorage |
| **WhatsApp integration** | Pre-filled order links, floating WhatsApp button |
| **Responsive design** | Bootstrap 5 + custom CSS, tested at 375px / 768px |
| **Django Admin** | Extended admin with cart sessions, inquiries, products |
| **REST API** | DRF endpoints for products and cart (used by Vite frontend) |
| **React/Vite frontend** | Parallel SPA at `/frontend/` consuming the REST API |
| **Production deployment** | Render.com, PostgreSQL, WhiteNoise static files, gunicorn |
| **CI/CD** | GitHub Actions on push to main |
| **Project management** | Trello board with Epics, In Progress, Done, Capstone Assets |

### What's Planned / Out of Scope ⏳
| Area | Reason Not Implemented |
|------|------------------------|
| **Live payment processing** | Requires Pesapal/MTN Mobile Money merchant account (real business requirement) |
| **Email order confirmations** | Needs SMTP/SendGrid configuration — WhatsApp is the primary channel for this market |
| **Order history** | Shoppers signed in can use `/account/orders/`; admin manages order status |
| **Product reviews** | Model + admin exist; storefront depth varies by sprint |
| **Wishlist** | Planned in backlog |
| **Advanced search (Elasticsearch)** | Database ILIKE search is sufficient at current scale |

### Tech Stack Justification
- **Django** — Batteries-included MVC, excellent ORM, built-in auth and admin reduce boilerplate for a solo developer.
- **PostgreSQL (prod) / SQLite (dev)** — Production-grade relational DB; SQLite keeps local dev frictionless.
- **Django REST Framework** — Industry-standard for Django APIs; used for the React frontend integration.
- **React + Vite** — Modern frontend tooling; shows full-stack capability for the capstone.
- **Bootstrap 5** — Rapid responsive UI with well-known component library.
- **Render.com** — Free-tier deployment with PostgreSQL, easy git-push deploys, appropriate for capstone demo.
- **WhatsApp ordering** — Not a tech compromise; it's the dominant commerce channel in East Africa. 80%+ of small business orders in Uganda happen via WhatsApp.

### Business Context
- **Who:** Kistie Store is a real boutique concept for women's fashion in Kampala, Uganda.
- **What:** Premium imported fashion from Turkey, UK, and USA. EU sizing.
- **Why online:** Expand from walk-in / social media DM sales to structured e-commerce.
- **Payment reality:** MTN Mobile Money and Airtel Money are the primary payment methods; card payments are secondary. Sandbox integration is the next step once a merchant account is set up.
- **Sizing:** EU sizing is used because stock is sourced from European/Turkish suppliers — this is explicitly communicated throughout the UI to reduce returns.

---

## Q&A Prep

**Q: Why two frontends (Django templates + React)?**  
A: The Django templates frontend is the primary production app. The React/Vite frontend demonstrates full-stack API skills and would be the path for a future native mobile app.

**Q: How does the cart work without login?**  
A: Django's session framework creates an anonymous session cookie. The cart is stored server-side keyed to that session. On login, the session can be merged with the user account.

**Q: How would you scale this?**  
A: Add Redis for sessions/cache, move media to S3/Cloudinary, add a CDN in front of Render, and separate the API from the admin with rate limiting.

**Q: What's the biggest technical challenge you solved?**  
A: The CSV import/export for inventory — parsing user-uploaded files, validating each row, mapping to Django models, handling image references, and giving line-by-line error feedback without crashing on bad data.

---

## Submission Checklist
- [x] Live URL in README: https://kristie-store.onrender.com
- [x] GitHub repo: https://github.com/dallas8000-ops/Kistie-Store
- [x] Trello board: https://trello.com/b/s8Rpm9in/kistie-store
- [x] Planning doc: PROJECT_PLANNING.md
- [x] Screenshots: `images/screenshots/` (and **embedded in the submitted capstone document**)
- [x] README: Pages & Features table, quick-links, setup instructions, reviewer access note
- [ ] Final cover sheet / submission form (per instructor requirements)
