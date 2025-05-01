// Estructura para ambos proyectos

// 1. Chatbot Widget - Vue + TypeScript
// File: chatbot-frontend/src/components/ChatWidget.vue
<template>
  <div class="rounded-2xl shadow-lg p-4 w-full max-w-sm bg-blue-700 text-white font-montserrat">
    <h2 class="text-xl font-bold mb-2">Chat Legal</h2>
    <div class="h-60 overflow-y-auto bg-blue-800 p-2 rounded-md mb-2">
      <div v-for="(msg, i) in mensajes" :key="i" class="mb-1">
        <strong>{{ msg.rol }}:</strong> {{ msg.texto }}
      </div>
    </div>
    <input
      v-model="pregunta"
      @keydown.enter="enviar"
      class="w-full p-2 rounded-md text-black"
      placeholder="Escribe tu consulta..."
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import axios from 'axios';

const mensajes = ref<{ rol: string; texto: string }[]>([]);
const pregunta = ref('');

const enviar = async () => {
  if (!pregunta.value.trim()) return;
  mensajes.value.push({ rol: 'Usuario', texto: pregunta.value });
  const { data } = await axios.post('http://localhost:5000/chat', { pregunta: pregunta.value });
  mensajes.value.push({ rol: 'Bot', texto: data.respuesta });
  pregunta.value = '';
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
.font-montserrat {
  font-family: 'Montserrat', sans-serif;
}
</style>

// 2. Document Analyzer - App.vue (frontend)
// File: analyzer-frontend/src/App.vue
<template>
  <div class="bg-blue-900 min-h-screen text-white font-montserrat p-6">
    <h1 class="text-3xl font-bold mb-6">Análisis y Clasificación Legal de Documentos</h1>
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-4">
      <div class="lg:col-span-1">
        <button
          v-for="n in 7"
          :key="n"
          class="bg-blue-600 hover:bg-blue-700 w-full mb-2 p-2 rounded-xl"
          @click="seleccionarArchivo(n - 1)"
        >
          Cargar PDF {{ n }}
        </button>
      </div>
      <div class="lg:col-span-3 bg-blue-800 p-4 rounded-xl">
        <div v-if="archivos.length" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div v-for="(archivo, i) in archivos" :key="i" class="bg-white text-black p-3 rounded-md">
            <strong>{{ archivo.name }}</strong>
          </div>
        </div>
        <div v-else class="text-gray-300">Selecciona archivos para comenzar</div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
const archivos = ref<(File | undefined)[]>([]);

const seleccionarArchivo = (index: number) => {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'application/pdf';
  input.onchange = () => {
    const file = input.files?.[0];
    if (file) archivos.value[index] = file;
  };
  input.click();
};
</script>

<style scoped>
.font-montserrat {
  font-family: 'Montserrat', sans-serif;
}
</style>
