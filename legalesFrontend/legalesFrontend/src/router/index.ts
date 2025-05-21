// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../components/loginPage.vue'
import DocumentAnalysis from '../components/Documentos.vue'
import AudioToText from '../components/AudioToText.vue'

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

router.beforeEach((to, from, next) => {
  const autenticado = localStorage.getItem('autenticado') === 'true'

  if (to.meta.requiresAuth && !autenticado) {
    next('/login')
  } else {
    next()
  }
})

export default router


