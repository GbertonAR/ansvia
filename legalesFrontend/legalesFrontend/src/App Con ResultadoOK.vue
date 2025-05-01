<template>
  <div class="min-h-screen bg-blue-800 text-white font-[Montserrat] flex">
    <!-- Menú lateral -->
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

    <!-- Contenido principal -->
    <main class="flex-1 p-10">
      <h1 class="text-3xl font-bold mb-2">Análisis de Documentación</h1>
      <p class="mb-6 text-blue-200">Selecciona archivos PDF desde la columna izquierda.</p>

      <div v-if="archivosSeleccionados.length > 0" class="mb-8">
        <h2 class="text-lg font-semibold mb-2">Archivos seleccionados:</h2>
        <ul class="list-disc pl-5 space-y-1 text-blue-100 text-sm">
          <li v-for="(archivo, index) in archivosSeleccionados" :key="index">
            {{ archivo?.name }}
          </li>
        </ul>
      </div>

      <div class="bg-blue-700 p-6 rounded-lg shadow-md max-w-2xl">
        <QuestionForm @enviar-consulta="enviarAnalisis" />
      </div>

      <div v-if="respuestaBackend" class="mt-10 bg-blue-700 p-6 rounded-lg">
        <div class="flex justify-between items-center mb-2">
          <h2 class="text-2xl font-semibold">📄 Resultado</h2>
          <button @click="mostrarResultado = !mostrarResultado" class="text-sm bg-blue-600 hover:bg-blue-500 px-3 py-1 rounded">
            {{ mostrarResultado ? 'Ocultar' : 'Mostrar' }}
          </button>
        </div>
        <div v-if="mostrarResultado" class="max-h-96 overflow-y-auto bg-blue-800 p-4 rounded mt-2">
          <p class="text-blue-100 text-sm mb-2">
            <strong>Archivo:</strong> {{ archivosSeleccionados[0]?.name || 'Sin nombre' }}
          </p>
          <div v-html="resaltarPalabrasClave(respuestaBackend.answer)" class="text-white space-y-2"></div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import QuestionForm from './components/QuestionForm.vue'
import axios from 'axios'

const archivosSeleccionados = ref<(File | undefined)[]>([])
const respuestaBackend = ref<any>(null)
const mostrarResultado = ref(true)
const backendUrl = 'http://localhost:5000/ask'

const seleccionarArchivo = (index: number) => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'application/pdf'
  input.onchange = (event: Event) => {
    const files = (event.target as HTMLInputElement).files
    if (files?.length) archivosSeleccionados.value[index] = files[0]
  }
  input.click()
}

const enviarAnalisis = async (pregunta: string) => {
  const formData = new FormData()
  archivosSeleccionados.value.forEach((archivo) => {
    if (archivo) formData.append('archivos', archivo)
  })
  formData.append('pregunta', pregunta)

  try {
    const res = await axios.post(backendUrl, formData)
    console.log('Respuesta del backend:', res.data)
    respuestaBackend.value = res.data
  } catch (err: any) {
    console.error('Error al analizar:', err.message)
  }
}

const resaltarPalabrasClave = (texto: string): string => {
  const palabras = texto
    .toLowerCase()
    .replace(/[.,;()¿?¡!"“”]/g, '')
    .split(/\s+/)

  const frecuencia: Record<string, number> = {}
  for (const palabra of palabras) {
    if (palabra.length > 5) {
      frecuencia[palabra] = (frecuencia[palabra] || 0) + 1
    }
  }

  const topPalabras = Object.entries(frecuencia)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([palabra]) => palabra)

  const regex = new RegExp(`\\b(${topPalabras.join('|')})\\b`, 'gi')
  return texto.replace(regex, '<span class="text-yellow-400 font-semibold">$1</span>')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
</style>
