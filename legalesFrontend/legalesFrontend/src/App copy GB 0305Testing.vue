<template>
  <div class="min-h-screen bg-blue-100">
    <!-- Header -->
    <header class="bg-blue-600 py-6 shadow-md">
      <div class="max-w-6xl mx-auto px-4 tarjeta.titulo">
        <!-- <h1 class="text-3xl items-center --color-heading font-bold">Análisis de Documentación</h1> -->
        <!-- <h1 class="text-3xl font-bold text-align-center --color-blue">Análisis de Documentación</h1> -->
        <h1 class="titulo-azul-centrado">Análisis de Documentación</h1>
        <p class="titulo-azul-centrado">Sube tus documentos PDF y realiza consultas específicas sobre su contenido.</p>
      </div>
    </header>

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-8">
      <!-- Sección de subir PDFs -->
      <div class="bg-white p-6 rounded-xl shadow-md">
          <h2 class="text-xl font-semibold mb-4">Subir PDFs</h2>
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-4">
            <div class="flex flex-col gap-y-4">
                <button
                  v-for="(archivo, index) in archivosSeleccionados"
                  :key="index"
                  @click="seleccionarArchivo(index)"
                  class="h-16 w-full flex items-center justify-center border-2 border-dashed rounded-lg hover:bg-blue-50 transition text-sm text-gray-600"
                >
                  {{ archivo?.name || `PDF ${index + 1}` }}
                </button>
            </div>
          </div>
      </div>

      <!-- Sección de preguntas -->
      <div class="bg-white p-6 rounded-xl shadow-md">
          <h2 class="text-xl font-semibold mb-4">Ingrese su Pregunta</h2>
          <div class="flex flex-col sm:flex-row gap-4">
            <textarea
              v-model="pregunta"
              rows="3"
              placeholder="Escriba su pregunta sobre los documentos subidos..."
              class="flex-1 p-3 border rounded-md resize-none">
            </textarea>
            <button
              @click="enviarAnalisis"
              :disabled="procesando"
              class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              {{ procesando ? 'Analizando...' : 'Enviar para Análisis' }}
            </button>
          </div>
      </div>

      <!-- Sección de resultados -->
      <div class="bg-white p-6 rounded-xl shadow-md">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">Resultados del Análisis</h2>
          <button
            @click="descargarWord"
            class="text-sm bg-green-600 text-white px-4 py-1 rounded hover:bg-green-700"
            v-if="respuestaBackend"
          >
            Descargar Word
          </button>
        </div>
          <div v-if="respuestaBackend" class="prose max-w-none" v-html="resaltarPalabrasClave(respuestaBackend.answer)">
        </div>
        <div v-else class="text-gray-400 italic">No se ha recibido ninguna respuesta aún.</div>
      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const archivosSeleccionados = ref<(File | undefined)[]>(Array(7).fill(undefined))
const pregunta = ref('')
const respuestaBackend = ref<any>(null)
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

const enviarAnalisis = async () => {
  if (!pregunta.value.trim()) return

  procesando.value = true
  const formData = new FormData()
  archivosSeleccionados.value.forEach((archivo) => {
    if (archivo) formData.append('archivos', archivo)
  })
  formData.append('pregunta', pregunta.value)

  try {
    const res = await axios.post(backendUrl, formData)
    respuestaBackend.value = Array.isArray(res.data) ? res.data[0] ?? {} : res.data || { answer: 'Respuesta desconocida.' }
  } catch (err: any) {
    console.error('Error al analizar:', err.message)
    respuestaBackend.value = { answer: 'Error al procesar la solicitud.' }
  } finally {
    procesando.value = false
  }
}

const resaltarPalabrasClave = (texto: string): string => {
  const palabras = texto.toLowerCase().replace(/[.,;()¿?¡!"“”]/g, '').split(/\s+/)
  const frecuencia: Record<string, number> = {}
  for (const palabra of palabras) {
    if (palabra.length > 5) frecuencia[palabra] = (frecuencia[palabra] || 0) + 1
  }
  const topPalabras = Object.entries(frecuencia).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([p]) => p)
  const regex = new RegExp(`\\b(${topPalabras.join('|')})\\b`, 'gi')
  return texto.replace(regex, '<span class="bg-yellow-300 text-black font-bold px-1 rounded">$1</span>')
}

const descargarWord = () => {
  const contenido = respuestaBackend.value?.answer || ''
  const html = `<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'><head><meta charset='utf-8'><title>Documento</title></head><body>${contenido}</body></html>`
  const blob = new Blob(['\ufeff', html], { type: 'application/msword' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = 'resultado.doc'
  link.click()
}
</script>

<style scoped>
.prose :deep(span) {
  padding: 0.1rem 0.25rem;
  border-radius: 0.25rem;
}
</style>
