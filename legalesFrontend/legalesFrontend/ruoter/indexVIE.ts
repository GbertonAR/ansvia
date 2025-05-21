// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '@/components/LoginPage.vue'
import DocumentAnalysis from '@/views/DocumentAnalysis.vue'
import AudioToText from '@/views/AudioToText.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    redirect: '/login',
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
  },
  {
    path: '/documentos',
    name: 'Documentos',
    component: DocumentAnalysis,
    meta: { requiresAuth: true }
  },
  {
    path: '/audio',
    name: 'Audio',
    component: AudioToText,
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
