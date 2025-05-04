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
      <div>
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

          <button @click="descargarWord" class="mt-4 bg-white text-blue-600 px-4 py-2 rounded shadow">
            Descargar como Word
          </button>

          <div v-if="mostrarResultado" class="max-h-96 overflow-y-auto bg-blue-800 p-4 rounded mt-2">
            <p class="text-blue-100 text-sm mb-2">
              <strong>Archivo:</strong> {{ archivosSeleccionados[0]?.name || 'Sin nombre' }}
            </p>
            <div v-html="resaltarPalabrasClave(respuestaBackend?.answer || '')" class="text-white space-y-2"></div>
          </div>
        </div>
      </div>

      <!-- Pantalla de procesamiento -->
      <div v-if="procesando" class="absolute inset-0 bg-blue-950 bg-opacity-95 z-50 flex flex-col items-center justify-center text-center p-10">
        <div class="animate-pulse mb-6">🧠</div>
        <h2 class="text-2xl font-bold mb-4">Analizando documentos...</h2>
        <div class="w-full max-w-xl bg-blue-800 text-left text-sm p-4 rounded shadow-inner font-mono text-blue-200 overflow-y-auto h-48">
          <p>→ Conectando con IA legal...</p>
          <p>→ Cargando {{ archivosSeleccionados.length }} archivos PDF...</p>
          <p>→ Analizando sintaxis, contexto y legislación relacionada...</p>
          <p>→ Extrayendo artículos clave...</p>
          <p>→ Generando resumen inteligente...</p>
          <p class="text-yellow-300 mt-2">⚙️ Este proceso puede tardar unos segundos.</p>
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
const procesando = ref(false)
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
  procesando.value = true

  const formData = new FormData()
  archivosSeleccionados.value.forEach((archivo) => {
    if (archivo) formData.append('archivos', archivo)
  })
  formData.append('pregunta', pregunta)

  try {
    const res = await axios.post(backendUrl, formData)

    if (Array.isArray(res.data)) {
      respuestaBackend.value = res.data[0] ?? {}
    } else if (typeof res.data === 'object' && res.data !== null) {
      respuestaBackend.value = res.data
    } else {
      respuestaBackend.value = { answer: 'Respuesta en formato desconocido.' }
    }
  } catch (err: any) {
    console.error('Error al analizar:', err.message)
  } finally {
    procesando.value = false
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
  return texto.replace(
    regex,
    '<span class="bg-yellow-300 text-black font-bold px-1 rounded">$1</span>'
  )
}

const descargarWord = () => {
  const contenido = respuestaBackend.value?.answer || ''
  const titulo = 'resultado.doc'

  const html = `
    <html xmlns:o='urn:schemas-microsoft-com:office:office' 
          xmlns:w='urn:schemas-microsoft-com:office:word' 
          xmlns='http://www.w3.org/TR/REC-html40'>
    <head><meta charset='utf-8'><title>Documento</title></head>
    <body>${contenido}</body>
    </html>
  `
  const blob = new Blob(['\ufeff', html], {
    type: 'application/msword',
  })

  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = titulo
  link.click()
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
</style>
