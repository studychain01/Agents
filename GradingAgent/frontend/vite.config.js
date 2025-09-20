import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
export default defineConfig({
  plugins: [react()],
  preview: {
    host: "0.0.0.0",
    port: 4173,
    allowedHosts: ["5pbxzfbk9p.us-east-1.awsapprunner.com", "all"]
  },
  server: {
    host: "0.0.0.0",
    port: 4173,
    allowedHosts: ["5pbxzfbk9p.us-east-1.awsapprunner.com", "all"]
  }
});
