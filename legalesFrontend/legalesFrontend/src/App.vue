<template>
  <div class="min-h-screen bg-blue-800 text-white font-[Montserrat] flex">
    <!-- Menú lateral -->
    <aside class="w-64 bg-blue-900 p-6 shadow-lg flex flex-col">
      <h2 class="text-xl font-bold mb-6 flex items-center gap-2">
        📁 Documentos
      </h2>
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
            {{ archivo.name }}
          </li>
        </ul>
      </div>

      <div class="bg-blue-700 p-6 rounded-lg shadow-md max-w-2xl">
        <QuestionForm @enviar-consulta="enviarAnalisis" />
      </div>

      <div v-if="respuestaBackend" class="mt-10 bg-blue-700 p-6 rounded-lg">
        <h2 class="text-2xl font-semibold mb-4">📄 Resultados</h2>
        <div
          v-for="(resultado, index) in respuestaBackend"
          :key="index"
          class="mb-4 border-b border-blue-400 pb-2"
        >
          <p><strong>Archivo:</strong> {{ resultado.archivo }}</p>
          <p><strong>Página:</strong> {{ resultado.pagina }}</p>
          <p><strong>Párrafo:</strong> {{ resultado.parrafo }}</p>
          <p><strong>Respuesta:</strong> {{ resultado.respuesta }}</p>
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
const backendUrl = 'http://localhost:5000/analizar'

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
    respuestaBackend.value = res.data
  } catch (err: any) {
    console.error('Error al analizar:', err.message)
  }
}
</script>

<style scoped>
/* Fondo Montserrat global si no está ya configurado */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
</style>
