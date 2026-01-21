import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path';

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  server: {
    // Optional: change the Vite dev‑server port (default 5173)
    // port: 3000,

  // Proxy rules
  proxy: {
    // All requests that start with /api/ will be forwarded.
    // The `changeOrigin` flag makes the Host header match the target.
    '/api': {
      target: `http://localhost:11354`,
      changeOrigin: true,
      // If your backend does not serve the `/api` prefix itself,
      // you can strip it with `rewrite`.  In most cases you keep it.
      rewrite: (path) => path.replace(/^\/api/, '/api'),
      secure: false,          // ignore self‑signed certs (if you ever use https)
      ws: true,               // enable websockets proxying (optional)
    },
  },
}
})
