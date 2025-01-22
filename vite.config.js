import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  base: './', // ✅ This ensures Vite uses relative paths for assets
  build: {
    outDir: path.resolve(__dirname, '../backend/static'), // ✅ Flask serves from `backend/static`
    emptyOutDir: true, // ✅ Clears old build files before building
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000', // ✅ Flask API proxy in development
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
