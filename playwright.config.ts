import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './browser_use_ext/tests/e2e', // Point to your E2E test directory
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you clone the snapshots */
  // For visual regression, uncomment the following line
  // expect: {
  //   toHaveScreenshot: {
  //     maxDiffPixels: 100,
  //     maxDiffPixelRatio: 0.01,
  //     animations: 'disabled',
  //     caret: 'hide',
  //   },
  // },
  /* Reporter to use. See https://playwright.dev/docs/reporters */
  reporter: 'html',
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    // baseURL: 'http://127.0.0.1:3000',

    /* Collect traces on failure. See https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },

    // For cross-browser testing, uncomment and configure other browsers
    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'] },
    // },
    // {
    //   name: 'webkit',
    //   use: { ...devices['Desktop Safari'] },
    // },

    /* Test against mobile viewports. */
    // { name: 'Mobile Chrome', use: { ...devices['Pixel 5'] } },
    // { name: 'Mobile Safari', use: { ...devices['iPhone 12'] } },

    /* Test against branded browsers. */
    // { name: 'Microsoft Edge', use: { ...devices['Desktop Edge'], channel: 'msedge' } },
    // { name: 'Google Chrome', use: { ...devices['Desktop Chrome'], channel: 'chrome' } },
  ],

  /* Run your local dev server before starting the tests */
  // webServer: {
  //   command: 'npm run start',
  //   url: 'http://127.0.0.1:3000',
  //   reuseExistingServer: !process.env.CI,
  // },

  // Configure Cucumber for BDD if desired
  // cucumberOpts: {
  //   require: ['./browser_use_ext/tests/e2e/step_definitions/*.ts'],
  //   format: ['html:./reports/cucumber.html'],
  // },
}); 