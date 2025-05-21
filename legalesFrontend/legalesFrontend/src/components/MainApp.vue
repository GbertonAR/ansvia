<template>
  <div>
    <!-- Página de Login -->
    <router-view v-if="!autenticado" />

    <!-- Aplicación principal -->
    <div v-else class="min-h-screen bg-blue-800 text-white font-[Montserrat] flex flex-col">
      <!-- HEADER SUPERIOR -->
      <header class="h-1/4 flex flex-col justify-center items-center bg-blue-900 shadow-md p-6">
        <h1 class="text-3xl font-bold mb-2">Análisis de Documentación</h1>
        <p class="text-sm">Hoy es {{ fechaHoy }} - {{ saludo }}</p>
      </header>

      <!-- MENÚ HORIZONTAL -->
      <nav class="flex justify-center bg-blue-700 py-3 space-x-4 shadow">
        <router-link to="/app/documentos" class="px-4 py-2 bg-purple-600 hover:bg-purple-500 rounded text-white">
          Documentos
        </router-link>
        <router-link to="/app/audio" class="px-4 py-2 bg-purple-600 hover:bg-purple-500 rounded text-white">
          Audio a Texto
        </router-link>
        <button class="px-4 py-2 bg-purple-600 hover:bg-purple-500 rounded text-white">Opción 3</button>
        <button class="px-4 py-2 bg-purple-600 hover:bg-purple-500 rounded text-white">Opción 4</button>
      </nav>

      <!-- CONTENIDO PRINCIPAL -->
      <div class="flex flex-1 overflow-hidden">
        <!-- LATERAL IZQUIERDO -->
        <aside class="w-64 bg-blue-900 p-6 shadow-lg flex flex-col">
          <h2 class="text-xl font-bold mb-6 flex items-center gap-2">📁 Documentos</h2>
          <div class="space-y-3">
            <button
              v-for="n in 7"
              :key="n"
              class="w-full py-2 px-4 bg-blue-600 hover:bg-blue-500 rounded-lg transition text-sm"
              @click="seleccionarArchivo(n - 1)"
            >
              Subir PDF {{ n }}
            </button>
          </div>
        </aside>

        <!-- AREA DE PREGUNTA + RESULTADO -->
        <main class="flex-1 p-10 overflow-y-auto">
          <router-view />
        </main>
      </div>

      <FooterComponent />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'
import FooterComponent from './components/FooterComponent.vue'
import LoginPage from './components/loginPage.vue'
import AudioToText from './components/AudioToText.vue'
import { useRouter } from 'vue-router'

const autenticado = ref(false)

// Utilidades de fecha y saludo
const fechaHoy = new Date().toLocaleDateString()
const saludo = computed(() => {
  const hora = new Date().getHours()
  if (hora < 12) return 'Buenos días'
  else if (hora < 18) return 'Buenas tardes'
  return 'Buenas noches'
})
</script>
