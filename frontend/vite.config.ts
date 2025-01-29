import { fileURLToPath, URL } from 'node:url';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// Create a function to set the environment in the define block
function getDefineEnv() {
  if (process.env.NODE_ENV === 'production') {
    return 'production';
  } else {
    return 'development';
  }
}

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  test: {
    globals: true,
    environment: 'happy-dom',
  },
  define: {
    // Set process.env.NODE_ENV based on the environment variable
    'process.env.NODE_ENV': JSON.stringify(getDefineEnv()),
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
  },
});
