import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 360000,
  use: {
    baseURL: 'http://127.0.0.1:8000',
    headless: false,
    slowMo: 2000,
    viewport: { width: 1280, height: 800 },
    video: 'off',
    screenshot: 'off',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], slowMo: 2000 },
    },
  ],
});
