// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import DocumentosView from '@/views/DocumentosView.vue'
import AudioTextoView from '@/views/AudioTextoView.vue'

const routes = [
  { path: '/', redirect: '/documentos' },
  { path: '/documentos', component: DocumentosView },
  { path: '/audio-texto', component: AudioTextoView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
