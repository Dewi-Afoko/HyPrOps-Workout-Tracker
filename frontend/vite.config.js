import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [react()],
    test: {
    globals: true,              // Use global test APIs like `describe`, `it`, `expect`
    environment: 'jsdom',       // Simulates a browser-like environment
    setupFiles: './setupTests.js', // Include additional setup (e.g., mocks)
},
});
