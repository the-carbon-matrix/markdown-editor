import { fileURLToPath, URL } from 'node:url'
import process from 'node:process'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

process.loadEnvFile('../.env')

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: process.env.BACKEND_URL,
        changeOrigin: true,
      },
      '/login': {
        target: process.env.BACKEND_URL,
        changeOrigin: true,
      },
      '/logout': {
        target: process.env.BACKEND_URL,
        changeOrigin: true,
      },
      '/register': {
        target: process.env.BACKEND_URL,
        changeOrigin: true,
      },
      '/refresh-token': {
        target: process.env.BACKEND_URL,
        changeOrigin: true,
      },
    },
  },
  build: {
    manifest: true,
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
