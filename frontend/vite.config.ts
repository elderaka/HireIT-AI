import { defineConfig } from "vite";
import tailwindcss from '@tailwindcss/vite'
import vue from "@vitejs/plugin-vue";
import path from 'path';

export default defineConfig({
  plugins: [
    tailwindcss(),
    vue()
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    proxy: {
      "/api": "http://localhost:3001"
    }
  }
})