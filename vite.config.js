import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
    port: 5173,  // you can change the port if needed
},
resolve: {
    alias: {
      '@': '/src',  // allows for `@/component` style imports
    },
},
build: {
    outDir: 'build',  // where Vite will output the build files
},
  // Define environment variables (optional)
define: {
    'process.env': process.env,  // Pass all environment variables as process.env (for compatibility)
},
});
