import { test, expect } from "@playwright/test";

test("top-level navigation renders", async ({ page }) => {
  await page.goto("/");
  const nav = page.getByRole("navigation");
  await expect(nav.getByRole("link", { name: "Bridge" })).toBeVisible();
  await expect(nav.getByRole("link", { name: "Atlas Maps" })).toBeVisible();
  await expect(nav.getByRole("link", { name: "AI Chat" })).toBeVisible();
  await expect(nav.getByRole("link", { name: "Field Guide" })).toBeVisible();
  await expect(nav.getByRole("link", { name: "Control Room" })).toBeVisible();
});
