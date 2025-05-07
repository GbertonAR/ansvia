<template>
  <div class="min-h-screen bg-blue-800 text-white font-[Montserrat] flex flex-col">

    <!-- HEADER SUPERIOR -->
    <header class="h-1/4 flex flex-col justify-center items-center bg-blue-900 shadow-md p-6">
      <h1 class="text-3xl font-bold mb-2">Análisis de Documentación</h1>
      <p class="text-sm">Hoy es {{ fechaHoy }} - {{ saludo }}</p>
    </header>

    <!-- MENÚ HORIZONTAL -->
    <nav class="flex justify-center bg-blue-700 py-3 space-x-4 shadow">
      <button class="px-4 py-2 bg-purple-600 hover:bg-purple-500 rounded text-white">Opción 1</button>
      <button class="px-4 py-2 bg-purple-600 hover:bg-purple-500 rounded text-white">Opción 2</button>
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
        
        <div v-if="archivosSeleccionados.length > 0" class="mb-8">
          <h2 class="text-lg font-semibold mb-2">Archivos seleccionados:</h2>
          <ul class="list-disc pl-5 space-y-1 text-blue-100 text-sm">
            <li v-for="(archivo, index) in archivosSeleccionados" :key="index">
              {{ archivo?.name }}
            </li>
          </ul>
        </div>

        <div class="bg-blue-700 p-6 rounded-lg shadow-md max-w-2xl mb-8">
          <QuestionForm @enviar-consulta="enviarAnalisis" />
        </div>

        <!-- Barra de progreso animada y curva -->
        <div v-if="cargando" class="relative h-3 overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-r from-cyan-300 via-white to-cyan-300 animate-loading-bar rounded-b-full"></div>
        </div>

        <!-- BARRA DE PROGRESO -->
        <div v-if="cargando" class="progress-bar fixed top-0 left-0 w-full z-50">
          <div class="progress-fill"></div>
        </div>

        <div v-if="respuestaBackend" class="bg-blue-700 p-6 rounded-lg shadow-md">
          <div class="flex justify-between items-center mb-2">
            <h2 class="text-2xl font-semibold">📄 Resultado</h2>
            <button @click="mostrarResultado = !mostrarResultado" class="text-sm bg-blue-600 hover:bg-blue-500 px-3 py-1 rounded">
              {{ mostrarResultado ? 'Ocultar' : 'Mostrar' }}
            </button>
          </div>

          <button @click="descargarWord" class="mt-4 bg-white text-blue-600 px-4 py-2 rounded shadow">
              Descargar como Word
          </button>

          <div v-if="mostrarResultado" class="max-h-96 overflow-y-auto bg-blue-800 p-4 rounded mt-4">
            <p class="text-blue-100 text-sm mb-2">
              <strong>Archivo:</strong> {{ archivosSeleccionados[0]?.name || 'Sin nombre' }}
            </p>
            <!-- <div v-html="resaltarPalabrasClave(respuestaBackend.answer)" class="text-white space-y-2"></div> -->
            <div v-html="resaltarYFormatearTexto(respuestaBackend.answer)" class="text-white"></div>
          </div>
        </div>

      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
// import { ref, computed } from 'vue'
import { ref, computed, nextTick } from 'vue'; // Importa nextTick aquí
import QuestionForm from './components/QuestionForm.vue'
import axios from 'axios'

const archivosSeleccionados = ref<(File | undefined)[]>([])
const respuestaBackend = ref<any>(null)
const mostrarResultado = ref(true)
const cargando = ref(false)  // NUEVO: estado para mostrar la barra de carga
// // const backendUrl = 'http://localhost:5000/ask'
// let backendUrl = import.meta.env.VITE_BACKEND_URL;
// if (import.meta.env.MODE === 'development') {
//   console.log("Modo desarrollo");
//   const backendUrl = 'http://localhost:5000/ask';
// } else {
//   console.log("Modo producción");
// }
let backendUrl = import.meta.env.VITE_BACKEND_URL;

if (import.meta.env.MODE === 'development') {
  console.log("Modo desarrollo");
  backendUrl = 'http://localhost:5000/ask';
} else {
  console.log("Modo producción");
}

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
  cargando.value = true  // INICIA la barra
  const formData = new FormData()
  archivosSeleccionados.value.forEach((archivo) => {
    if (archivo) formData.append('archivos', archivo)
  })
  formData.append('pregunta', pregunta)

  try {
    const res = await axios.post(backendUrl, formData)
    respuestaBackend.value = res.data
    await nextTick()
  } catch (err: any) {
    console.error('Error al analizar:', err.message)
  } finally {
    cargando.value = false  // TERMINA la barra
  }
}

const resaltarYFormatearTexto = (texto: string): string => {
  if (!texto) return '';

  const palabras = texto
    .toLowerCase()
    .replace(/[.,;()¿?¡!"“”]/g, '')
    .split(/\s+/)

  const frecuencia: Record<string, number> = {};
  for (const palabra of palabras) {
    if (palabra.length > 5) {
      frecuencia[palabra] = (frecuencia[palabra] || 0) + 1;
    }
  }

  const topPalabras = Object.entries(frecuencia)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([palabra]) => palabra);

  const regex = new RegExp(`\\b(${topPalabras.join('|')})\\b`, 'gi');

  // Separar en párrafos por doble salto o salto simple
  const parrafos = texto.split(/\n{1,2}/).filter(p => p.trim() !== '');

  // Convertir cada párrafo a HTML
  return parrafos.map(p => {
    const textoResaltado = p.replace(regex, '<span class="text-yellow-400 font-semibold">$1</span>');
    return `<p class="mb-4">${textoResaltado}</p>`;
  }).join('');
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

// Utilidades de fecha y saludo
const fechaHoy = new Date().toLocaleDateString()
const saludo = computed(() => {
  const hora = new Date().getHours()
  if (hora < 12) return 'Buenos días'
  else if (hora < 18) return 'Buenas tardes'
  return 'Buenas noches'
})

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
  const blob = new Blob(['\ufeff', html], { type: 'application/msword' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = titulo
  link.click()
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
</style>
