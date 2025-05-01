<template>
    <div class="min-h-screen bg-blue-800 text-white font-[Montserrat] flex">
      <!-- Menú lateral -->
      <aside class="w-64 bg-blue-900 p-6 shadow-lg flex flex-col">
        <h2 class="text-xl font-bold mb-6">📁 Documentos</h2>
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
      <main class="flex-1 p-10 overflow-auto">
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
  
        <div class="bg-blue-700 p-6 rounded-lg shadow-md max-w-2xl mb-10">
          <QuestionForm @enviar-consulta="enviarAnalisis" />
        </div>
  
        <div v-if="respuestaBackend.length > 0" class="bg-blue-700 p-6 rounded-lg shadow-md max-w-4xl relative">
          <h2 class="text-2xl font-semibold mb-4">📄 Resultados del Análisis</h2>
  
          <div class="overflow-y-auto max-h-[400px] pr-4">
            <div v-for="(r, idx) in respuestaBackend" :key="idx" class="mb-6 border-b border-blue-400 pb-4">
              <h3 class="text-lg font-bold text-yellow-300 mb-2">📎 {{ r.archivo || 'Archivo desconocido' }}</h3>
              <p v-html="resaltarPalabrasClave(r.respuesta)" class="text-white text-sm leading-relaxed"></p>
            </div>
          </div>
  
          <button
            @click="descargarWord"
            class="mt-4 bg-yellow-400 hover:bg-yellow-300 text-blue-900 px-4 py-2 rounded-lg font-semibold transition"
          >
            Descargar Word
          </button>
        </div>
      </main>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import axios from 'axios'
  import QuestionForm from './components/QuestionForm.vue'
  
  const archivosSeleccionados = ref<(File | undefined)[]>([])
  const respuestaBackend = ref<any[]>([])
  const backendUrl = 'http://localhost:5000/ask'
  
  // Selección de archivos
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
  
  // Envío de archivos + pregunta
  const enviarAnalisis = async (pregunta: string) => {
    const formData = new FormData()
    archivosSeleccionados.value.forEach((archivo) => {
      if (archivo) formData.append('archivos', archivo)
    })
    formData.append('pregunta', pregunta)
  
    try {
      const res = await axios.post(backendUrl, formData)
      console.log('Respuesta del backend:', res.data)
  
      if (Array.isArray(res.data)) {
        respuestaBackend.value = res.data
      } else {
        console.warn('Formato inesperado en respuesta')
        respuestaBackend.value = []
      }
    } catch (err) {
      console.error('Error al analizar:', err)
      respuestaBackend.value = []
    }
  }
  
  // Resaltado de palabras clave
  const resaltarPalabrasClave = (texto: string): string => {
    const palabras = texto
      .toLowerCase()
      .replace(/[.,;()¿?¡!"']/g, '')
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
      .map(([p]) => p)
  
    const regex = new RegExp(`\\b(${topPalabras.join('|')})\\b`, 'gi')
    return texto.replace(regex, '<span class="bg-yellow-400 text-blue-900 font-bold px-1 rounded">$1</span>')
  }
  
  // Exportar Word
  const descargarWord = () => {
    if (!respuestaBackend.value.length) {
      alert('No hay contenido para exportar.')
      return
    }
  
    let contenido = ''
    respuestaBackend.value.forEach((r) => {
      contenido += `📎 Archivo: ${r.archivo || 'desconocido'}\n\n${r.respuesta}\n\n\n`
    })
  
    const blob = new Blob([contenido], { type: 'application/msword' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = 'analisis.doc'
    link.click()
  }
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
  </style>
  