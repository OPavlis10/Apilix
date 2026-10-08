import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// /api is proxied to Django (python manage.py runserver -> :8000)
export default defineConfig({
  plugins: [react()],
  server: { proxy: { '/api': 'http://127.0.0.1:8000', '/admin': 'http://127.0.0.1:8000', '/static': 'http://127.0.0.1:8000' } },
});
