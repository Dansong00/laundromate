import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./src/__tests__/setup.ts"],
    include: ["**/*.test.{ts,tsx}"],
    exclude: ["node_modules", ".next", "dist"],
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: [
        "node_modules/",
        ".next/",
        "dist/",
        "**/*.test.{ts,tsx}",
        "**/__tests__/**",
        "**/*.config.{ts,js}",
      ],
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@laundromate/ui": path.resolve(
        __dirname,
        "../../packages/ui/src/index.ts",
      ),
      "@laundromate/types": path.resolve(
        __dirname,
        "../../packages/types/src/index.ts",
      ),
    },
  },
  css: {
    modules: {
      classNameStrategy: "non-scoped",
    },
    postcss: {
      plugins: [], // Use empty PostCSS plugins array to avoid loading postcss.config.mjs
    },
  },
});
