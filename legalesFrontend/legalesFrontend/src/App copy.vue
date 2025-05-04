<template>
  <div class="app-container">
    <header class="app-header">
      <h1 class="app-title">Análisis de Documentación</h1>
    </header>
    <main class="app-main">
      <div class="file-upload-area">
        <button
          v-for="(item, n) in archivosSeleccionados"
          :key="n"
          :class="[
              'w-full py-2 px-4 rounded-lg transition text-sm',
              item.cargado ? 'bg-green-600 hover:bg-green-500' : 'bg-blue-600 hover:bg-blue-500'
          ]"
              @click="seleccionarArchivo(n)"
          >
              {{ item.cargado ? 'PDF Cargado ✔️' : `Subir PDF ${n + 1}` }}
        </button>
        <!-- <button
          v-for="n in 7"
          :key="n"
          class="upload-button"
          @click="seleccionarArchivo(n - 1)"
        >
          Archivo PDF {{ n }}
        </button> -->
      </div>
      <div v-if="archivosSeleccionados.length > 0" class="preview-carousel">
        <div v-for="(archivo, index) in archivosSeleccionados" :key="index" class="file-preview">
          <p>{{ archivo.name }}</p>
        </div>
        <QuestionForm @enviar-consulta="enviarAnalisis" />
      </div>
      <div v-else class="placeholder-area">
        Seleccione archivos PDF utilizando los botones de la derecha.
      </div>
      <div v-if="respuestaBackend" class="results-display">
        <h2>Resultado del Análisis</h2>
        <div v-for="(resultado, index) in respuestaBackend" :key="index" class="resultado-item">
          <p><strong>Respuesta:</strong> {{ resultado.respuesta }}</p>
          <p><strong>Archivo:</strong> {{ resultado.archivo }}</p>
          <p><strong>Página:</strong> {{ resultado.pagina }}</p>
          <p><strong>Párrafo:</strong> {{ resultado.parrafo }}</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import QuestionForm from './components/QuestionForm.vue';
import axios from 'axios'; // Necesitamos Axios para las peticiones HTTP

// const archivosSeleccionados = ref<(File | undefined)[]>([]);
const archivosSeleccionados = ref(
  Array.from({ length: 7 }, () => ({
    archivo: undefined as File | undefined,
    cargado: false,
  }))
);
const archivosCargados = ref(false);
const respuestaBackend = ref<any>(null);
const backendUrl = 'http://localhost:5000/analizar'; // Reemplaza con la URL de tu backend

// const seleccionarArchivo = (index: number) => {
//   const input = document.createElement('input');
//   input.type = 'file';
//   input.accept = 'application/pdf';
//   input.multiple = false; // Permitir seleccionar un archivo por botón
//   input.onchange = (event: Event) => {
//     const files = (event.target as HTMLInputElement).files;
//     if (files && files.length > 0) {
//       // Asociar el archivo al botón correspondiente (podría ser más complejo si se permite reordenar)
//       if (!archivosSeleccionados.value[index]) {
//         archivosSeleccionados.value[index] = files[0];
//         // Verificar si todos los botones tienen un archivo (opcional)
//         archivosCargados.value = archivosSeleccionados.value.some(file => file !== undefined);
//       } else {
//         archivosSeleccionados.value[index] = files[0]; // Reemplazar si se selecciona otro archivo
//       }
//     }
//   };
//   input.click();
// };

const seleccionarArchivo = (index: number) => {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'application/pdf';
  input.multiple = false;
  input.onchange = (event: Event) => {
    const files = (event.target as HTMLInputElement).files;
    if (files && files.length > 0) {
      archivosSeleccionados.value[index].archivo = files[0];
      archivosSeleccionados.value[index].cargado = true;
    }
  };
  input.click();
};

const enviarAnalisis = async (pregunta: string) => {
  if (archivosSeleccionados.value.length > 0 && pregunta.trim() !== '') {
    const formData = new FormData();
    archivosSeleccionados.value.forEach(item => {
      // if (archivo) {
      //   formData.append('archivos', archivo);
      // }
      if (item.archivo) {
         formData.append('archivos', item.archivo);
      }
    });
    formData.append('pregunta', pregunta);

    try {
      const response = await axios.post(backendUrl, formData, {
        
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      respuestaBackend.value = response.data;
      console.log('Respuesta del backend:', response.data)
      console.log('Respuesta del backend:', formData)
    } catch (error: any) {
      console.error('Error al enviar los archivos y la pregunta:', error.message);
      alert('Error al procesar la solicitud. Por favor, inténtelo de nuevo.');
    }
  } else {
    alert('Por favor, cargue al menos un archivo PDF e ingrese su pregunta.');
  }
};

// Removed unused irAAnalisis function
</script>

<style scoped>
/* ... estilos anteriores ... */

.results-display {
  margin-top: 2em;
  padding: 1em;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 5px;
  width: 80%;
  max-width: 800px;
  color: white;
}

.resultado-item {
  margin-bottom: 1em;
  padding: 0.5em;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}
</style>