import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    rollupOptions: {
      onwarn(warning, warn) {
        // Skip TypeScript warnings during build
        if (warning.code === 'PLUGIN_WARNING') return
        warn(warning)
      }
    }
  },
  esbuild: {
    // Skip TypeScript type checking during build
    logOverride: { 'this-is-undefined-in-esm': 'silent' }
  }
})