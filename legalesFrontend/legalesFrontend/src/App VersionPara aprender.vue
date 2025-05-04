<template>
  <div class="min-h-screen bg-blue-50 font-[Montserrat] p-6 space-y-6">
    <!-- Header -->
    <header class="text-center">
      <h1 class="text-4xl font-bold text-blue-700">Análisis de Documentación</h1>
      <p class="text-gray-600 mt-2">Sube tus documentos PDF y realiza consultas específicas sobre su contenido.</p>
      <p class="text-sm text-gray-500 mt-1">
        {{ currentDate }} - 
        <span>{{ saludo }}</span>
      </p>
    </header>

    <!-- Secciones principales -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Tarjeta 1: Subida de PDFs -->
      <div class="bg-white shadow rounded-2xl p-4">
        <h2 class="text-lg font-semibold text-gray-800 mb-4">Subir PDFs</h2>
        <div class="grid grid-cols-2 gap-3">
          <button
            v-for="(pdf, index) in pdfButtons"
            :key="index"
            :class="pdf.uploaded ? 'bg-green-500' : 'bg-rose-300 hover:bg-rose-400'"
            @click="seleccionarArchivo(index)"
            class="text-white py-2 px-4 rounded transition"
          >
            {{ pdf.uploaded ? 'PDF ' + (index + 1) + ' Cargado' : 'Subir PDF ' + (index + 1) }}
          </button>
        </div>
      </div>

      <!-- Tarjeta 2: Pregunta -->
      <div class="bg-white shadow rounded-2xl p-4">
        <h2 class="text-lg font-semibold text-gray-800 mb-4">Ingrese su Pregunta</h2>
        <textarea 
          v-model="question"
          class="w-full h-32 p-3 border rounded resize-none text-gray-700 bg-gray-50"
          placeholder="Escriba su pregunta sobre los documentos..."
        ></textarea>
        <button 
          class="mt-4 bg-blue-600 hover:bg-blue-700 text-white py-2 px-6 rounded w-full transition" 
          @click="enviarAnalisis(question)"
        >
          Enviar para Análisis
        </button>
      </div>
    </div>

    <!-- Tarjeta 3: Resultados -->
    <div class="bg-white shadow rounded-2xl p-4 mt-4">
      <h2 class="text-lg font-semibold text-gray-800 mb-2">Resultados del Análisis</h2>
      <div v-if="procesando" class="text-gray-600">Procesando...</div>
      <div v-if="respuestaBackend && !procesando" class="text-gray-600" v-html="resaltarPalabrasClave(respuestaBackend?.answer)"></div>
      <button v-if="respuestaBackend" @click="descargarWord" class="mt-4 bg-green-600 hover:bg-green-700 text-white py-2 px-6 rounded">
        Descargar Resultado en Word
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Estados reactivos
const archivosSeleccionados = ref<(File | undefined)[]>([])
const respuestaBackend = ref<any>(null)
const procesando = ref(false)
const mostrarResultado = ref(true)
const question = ref('')
const isDesktop = ref(false)
const backendUrl = 'http://localhost:5000/ask'
const saludo = ref('')
const currentDate = new Date().toLocaleDateString()

// Lógica de la fecha y saludo según hora
onMounted(() => {
  const h = new Date().getHours()
  saludo.value = h < 12 ? "Buenos días" : h < 18 ? "Buenas tardes" : "Buenas noches"
  
  const checkScreen = () => {
    isDesktop.value = window.innerWidth >= 768
  }
  checkScreen()
  window.addEventListener('resize', checkScreen)
})

// Función para seleccionar un archivo PDF
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

// Función para enviar la consulta y los archivos al backend
const enviarAnalisis = async (pregunta: string) => {
  procesando.value = true
  const formData = new FormData()
  archivosSeleccionados.value.forEach((archivo) => {
    if (archivo) formData.append('archivos', archivo)
  })
  formData.append('pregunta', pregunta)

  try {
    const res = await axios.post(backendUrl, formData)
    respuestaBackend.value = Array.isArray(res.data) ? res.data[0] ?? {} : res.data || { answer: 'Respuesta desconocida.' }
  } catch (err: any) {
    console.error('Error al analizar:', err.message)
  } finally {
    procesando.value = false
  }
}

// Función para resaltar las palabras clave en el resultado
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

// Función para descargar el resultado como archivo Word
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
/* Estilos generales */
body {
  font-family: 'Montserrat', sans-serif;
}

/* Tarjetas */
.bg-white {
  background-color: #ffffff;
}

/* Sombra y bordes */
.shadow {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.rounded-2xl {
  border-radius: 1rem;
}

button {
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #f43f5e; /* color de hover */
}

/* Resaltado de palabras clave */
.bg-yellow-300 {
  background-color: #fef08a;
}

.text-black {
  color: black;
}
</style>
