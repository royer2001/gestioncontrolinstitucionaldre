import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/auth': 'http://localhost:5000',
      '/occurrence': 'http://localhost:5000',
      '/entry_exit': 'http://localhost:5000',
      '/visitor': 'http://localhost:5000',
      '/report': 'http://localhost:5000',
      '/vehicle': 'http://localhost:5000',
      '/citas': 'http://localhost:5000',
      '/license': 'http://localhost:5000',
      '/hr': 'http://localhost:5000',
      '/turn': 'http://localhost:5000',
    }
  }
})
