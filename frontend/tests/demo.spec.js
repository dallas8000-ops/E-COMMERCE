import { test, expect } from '@playwright/test';

// ── SET YOUR STAFF CREDENTIALS BELOW BEFORE RUNNING ──────────────────────────
const STAFF_USERNAME = 'KistieShopStaff';  // ← replace with your staff username
const STAFF_PASSWORD = 'UgandaPearl';  // ← replace with your staff password
// ─────────────────────────────────────────────────────────────────────────────

const DEMO_USER = `demo_kistie_${Date.now()}`;
const DEMO_PASS  = 'KistieDemo2026!';

test('Kistie Store — full presentation demo', async ({ page }) => {

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 1 — SHOP OVERVIEW & BILINGUAL UI
  // ══════════════════════════════════════════════════════════════════════════
  await page.goto('/shop/');
  await expect(page).toHaveTitle(/Shop.*Kistie Store/);
  await page.waitForTimeout(2500);

  // Luganda labels in navbar and shop heading
  await expect(page.locator('text=Ekyaguzi').first()).toBeVisible();
  await expect(page.locator('nav').getByText('Ekikapu')).toBeVisible();
  await expect(page.locator('nav').getByText('Ku Ffe')).toBeVisible();
  await page.waitForTimeout(2000);

  // Switch currency to UGX (local Ugandan shilling)
  await page.selectOption('#inventoryCurrency', 'UGX');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1500);

  // Switch payment to MTN Mobile Money
  await page.selectOption('#inventoryMethod', 'mtn');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1500);

  // Scroll through the product catalog
  await page.evaluate(() => window.scrollBy(0, 500));
  await page.waitForTimeout(2000);
  await page.evaluate(() => window.scrollBy(0, 500));
  await page.waitForTimeout(2000);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(1000);

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 2 — PRODUCT QUICK VIEW
  // ══════════════════════════════════════════════════════════════════════════
  const firstQuickView = page.locator('.quick-view-trigger').first();
  await firstQuickView.scrollIntoViewIfNeeded();
  await firstQuickView.click();
  await expect(page.locator('#productQuickViewModal')).toBeVisible();
  await page.waitForTimeout(3000);
  await page.locator('#productQuickViewModal .btn-close').click();
  await expect(page.locator('#productQuickViewModal')).toBeHidden();
  await page.waitForTimeout(1000);

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 3 — ADD TWO PRODUCTS TO CART
  // ══════════════════════════════════════════════════════════════════════════
  const inStockCards = page.locator('.inventory-shop-card').filter({ has: page.locator('.inventory-add-btn:not([disabled])') });
  const firstCard = inStockCards.first();
  await firstCard.scrollIntoViewIfNeeded();
  await firstCard.locator('select[name="size"]').selectOption({ index: 0 });
  await firstCard.locator('input[name="quantity"]').fill('1');
  await expect(firstCard.locator('text=Gattako mu Kikapu').first()).toBeVisible();
  await firstCard.locator('.inventory-add-btn').click();
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1500);

  // Navigate back to shop to add a second product
  await page.goto('/shop/?currency=UGX&payment_method=mtn');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1500);

  const inStockCards2 = page.locator('.inventory-shop-card').filter({ has: page.locator('.inventory-add-btn:not([disabled])') });
  const secondCard = inStockCards2.nth(1);
  await secondCard.scrollIntoViewIfNeeded();
  await secondCard.locator('select[name="size"]').selectOption({ index: 0 });
  await secondCard.locator('input[name="quantity"]').fill('1');
  await secondCard.locator('.inventory-add-btn').click();
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1500);

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 4 — CART: CURRENCY, PAYMENT METHOD, LUGANDA LABELS
  // ══════════════════════════════════════════════════════════════════════════
  await page.goto('/cart/');
  await expect(page.locator('h1')).toContainText('Your Cart');
  await expect(page.locator('text=Ekikapu Kyo')).toBeVisible();
  await page.waitForTimeout(2500);

  await page.selectOption('#cartCurrency', 'UGX');
  await page.selectOption('#cartMethod', 'mtn');
  await page.locator('button:has-text("Apply Checkout Settings")').click();
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(2000);

  await expect(page.locator('text=Enteeresa Yonna').first()).toBeVisible();
  await expect(page.locator('text=Nkola Omutendera').first()).toBeVisible();

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 5 — CHECKOUT & ORDER CONFIRMATION
  // ══════════════════════════════════════════════════════════════════════════
  await page.locator('a[href*="checkout"]').click();
  await page.waitForLoadState('networkidle');
  await expect(page.locator('h1')).toContainText('Checkout');
  await page.waitForTimeout(2000);

  await page.fill('#checkoutName', 'Nalwoga Sarah');
  await page.fill('#checkoutPhone', '+256 704 757198');
  await page.fill('#checkoutCountry', 'Uganda');
  await page.fill('#checkoutNotes', 'Deliver to Kampala — MTN payment');
  await page.waitForTimeout(1500);

  await page.locator('button.btn-brand-primary:has-text("Place Order")').click();
  await page.waitForLoadState('networkidle');

  await expect(page.locator('h1')).toContainText('Order Received');
  await expect(page.locator('text=Order Reference')).toBeVisible();
  await expect(page.locator('text=MTN').first()).toBeVisible();
  await page.waitForTimeout(4000);

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 6 — USER SIGNUP
  // ══════════════════════════════════════════════════════════════════════════
  await page.goto('/signup/');
  await expect(page.locator('h1')).toContainText('Create Your Shopper Account');
  await page.waitForTimeout(2000);

  await page.fill('#id_username', DEMO_USER);
  await page.fill('#id_password1', DEMO_PASS);
  await page.fill('#id_password2', DEMO_PASS);
  await page.locator('button:has-text("Create Account")').click();
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(2000);

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 7 — ORDER HISTORY (logged-in shopper view)
  // ══════════════════════════════════════════════════════════════════════════
  await page.goto('/account/orders/');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(3000);

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 8 — CONTACT PAGE & STORE INQUIRY
  // ══════════════════════════════════════════════════════════════════════════
  await page.goto('/contact/');
  await expect(page.locator('h1')).toContainText('Contact Kistie Store');
  await page.waitForTimeout(2000);

  await page.fill('#id_name', 'Nalwoga Sarah');
  await page.fill('#id_email', 'sarah@example.com');
  await page.fill('#id_subject', 'Bulk Order Inquiry — Kampala');
  await page.fill('#id_message', 'I would like to place a bulk order for 10 items. Please confirm availability.');
  await page.waitForTimeout(1500);

  await page.locator('button:has-text("Send Store Inquiry")').click();
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(2000);

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 9 — LOGOUT
  // ══════════════════════════════════════════════════════════════════════════
  await page.goto('/logout/');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(2000);
  // Clear session cookies to guarantee the shopper session is fully ended
  await page.context().clearCookies();

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 10 — STAFF LOGIN
  // ══════════════════════════════════════════════════════════════════════════
  await page.goto('/staff/login/');
  await expect(page.locator('h1')).toContainText('Staff sign in');
  await page.waitForTimeout(2000);

  await page.fill('#id_username', STAFF_USERNAME);
  await page.fill('#id_password', STAFF_PASSWORD);
  await page.locator('button:has-text("Staff sign in")').click();
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(2000);

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 11 — STAFF DASHBOARD: ORDERS, REVENUE, LOW STOCK
  // ══════════════════════════════════════════════════════════════════════════
  await expect(page.locator('h1')).toContainText('Staff dashboard');
  await page.waitForTimeout(3000);

  // Scroll to revenue table
  await page.evaluate(() => window.scrollBy(0, 400));
  await page.waitForTimeout(2500);

  // Scroll to low stock and inquiries
  await page.evaluate(() => window.scrollBy(0, 400));
  await page.waitForTimeout(2500);

  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(1500);

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 12 — INVENTORY API: PRODUCT & CATEGORY CATALOG (staff session)
  // ══════════════════════════════════════════════════════════════════════════
  await page.goto('/api/inventory/products/');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(3000);

  await page.evaluate(() => window.scrollBy(0, 400));
  await page.waitForTimeout(2000);

  await page.goto('/api/inventory/categories/');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(2500);

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 13 — ADMIN AUDIT LOG (superuser)
  // ══════════════════════════════════════════════════════════════════════════
  await page.goto('/staff/dashboard/');
  await page.waitForTimeout(1000);
  await page.locator('a:has-text("Admin audit log")').click();
  await page.waitForLoadState('networkidle');
  await expect(page.locator('h1')).toContainText('Admin audit log');
  await page.waitForTimeout(3000);

  await page.evaluate(() => window.scrollBy(0, 400));
  await page.waitForTimeout(2000);

  await page.locator('a:has-text("\u2190 Staff dashboard")').click();
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(2000);

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 14 — ABOUT PAGE & LUGANDA BRAND STORY
  // ══════════════════════════════════════════════════════════════════════════
  await page.goto('/about/');
  await expect(page.locator('text=Ku Kistie Store').first()).toBeVisible();
  await page.waitForTimeout(2000);
  await page.evaluate(() => window.scrollBy(0, 400));
  await page.waitForTimeout(2000);
  await expect(page.locator('text=Omulimu Gwaffe').first()).toBeVisible();
  await expect(page.locator('text=Empisa Za Ffwe').first()).toBeVisible();
  await page.waitForTimeout(2000);

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 15 — RETURN TO SHOP
  // ══════════════════════════════════════════════════════════════════════════
  await page.locator('a:has-text("Gula mu Kistie Store")').click();
  await page.waitForLoadState('networkidle');
  await expect(page).toHaveTitle(/Shop.*Kistie Store/);
  await page.waitForTimeout(3000);
});
