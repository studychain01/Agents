import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true
  },
  preview: {
    port: 4173,
    host: true,
    allowedHosts: [
      "dsdvaepmqx.us-east-2.awsapprunner.com",
      "*.awsapprunner.com",
      "all"
    ]
  },
  define: {
    __APP_VERSION__: JSON.stringify('1.0.0'),
  }
})

