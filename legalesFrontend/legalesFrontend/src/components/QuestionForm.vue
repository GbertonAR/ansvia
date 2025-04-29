<template>
    <div class="question-form">
      <h2>Ingrese su Pregunta</h2>
      <textarea
        v-model="pregunta"
        placeholder="Escriba aquí su pregunta sobre los documentos..."
        rows="4"
        class="question-input"
      ></textarea>
      <button @click="enviarConsulta" class="submit-button" :disabled="!pregunta.trim()">
        Enviar para Análisis
      </button>
    </div>
  </template>
  
  <script setup lang="ts">
  // import { ref, defineEmits } from 'vue';
  import { ref } from 'vue';
  
  const pregunta = ref('');
  const emit = defineEmits(['enviar-consulta']);
  
  const enviarConsulta = () => {
    if (pregunta.value.trim() !== '') {
      emit('enviar-consulta', pregunta.value);
      pregunta.value = ''; // Limpiar el campo después de enviar
    } else {
      alert('Por favor, ingrese su pregunta.');
    }
  };
  </script>
  
  <style scoped>
  .question-form {
    margin-top: 2em;
    padding: 1em;
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 5px;
    width: 80%;
    max-width: 600px;
    color: white;
    display: flex;
    flex-direction: column;
    gap: 1em;
  }
  
  h2 {
    margin-top: 0;
    color: white;
    text-align: center;
  }
  
  .question-input {
    padding: 0.8em;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 3px;
    background-color: rgba(0, 0, 0, 0.2);
    color: white;
    font-size: 1em;
    resize: vertical;
  }
  
  .submit-button {
    padding: 0.8em 1.5em;
    border: none;
    border-radius: 5px;
    background-color: #4caf50;
    color: white;
    font-size: 1em;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .submit-button:hover {
    background-color: #45a049;
  }
  
  .submit-button:disabled {
    background-color: gray;
    cursor: not-allowed;
  }
  </style>