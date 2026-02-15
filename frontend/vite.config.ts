import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [tailwindcss(), react(), tsconfigPaths()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    watch: {
      ignored: ["**/node_modules/**", "**/dist/**"],
    },
  },
});
