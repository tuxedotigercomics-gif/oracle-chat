import { defineConfig } from 'vite'

export default defineConfig({
  // Relative paths so the built site works from any folder / file:// as well.
  base: './',
  server: { port: 5173, open: true },
})
