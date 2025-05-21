<!-- src/components/AudioToText.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-800 to-blue-600 text-white flex flex-col items-center p-8">
    <h1 class="text-4xl font-bold mb-4 animate-fade-in">🎙️ Transcriptor Inteligente de Audio a Texto</h1>
    <p class="text-lg mb-6 text-center max-w-xl animate-fade-in delay-200">
      Carga un archivo de audio o pega el link de un video. Nuestro sistema extraerá el texto para que puedas analizarlo con facilidad.
    </p>

    <div class="bg-white bg-opacity-10 p-6 rounded-2xl shadow-lg w-full max-w-md space-y-4 animate-slide-in">
      <label class="block text-blue">
        <div class="bg-blue">
            <span class="text-black font-semibold">🎧 Link de YouTube o archivo .mp3:</span>
            <input
            v-model="link"
            type="text"
            placeholder="https://www.youtube.com/watch?v=..."
            class="mt-1 w-full p-2 rounded text-black bg-blue bg-opacity-20 border border-blue placeholder-blue focus:outline-none"
            />
        </div>
      </label>

      <label class="block">
        <span class="text-black font-semibold">📁 O selecciona un archivo de audio:</span>
        <input
          type="file"
          @change="handleFile"
          accept="audio/*"
          class="mt-1 w-full text-black"
        />
      </label>

      <button
        @click="startTranscription"
        :disabled="loading"
        class="w-full bg-white text-blue-800 font-bold py-2 rounded hover:bg-blue-200 transition disabled:opacity-50"
      >
        🔍 Transcribir
      </button>
    </div>

    <div v-if="loading" class="mt-8 flex items-center space-x-3">
      <svg class="animate-spin h-6 w-6 text-black" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="white" stroke-width="4"></circle>
        <path class="opacity-75" fill="white" d="M4 12a8 8 0 018-8v8H4z"></path>
      </svg>
      <p>Transcribiendo audio, por favor espera...</p>
    </div>

    <div v-if="transcription" class="mt-8 max-w-3xl bg-white bg-opacity-20 p-6 rounded-2xl shadow-lg">
      <!-- <h2 class="text-2xl color-black font-bold mb-2">📜 Resultado:</h2> -->
        <div class="text-black">
            <h2 class="text-2xl ">📜 Resultado:</h2>
            <pre class="whitespace-pre-wrap text-black">{{ transcription }}</pre>
        </div>
    </div>

    <video
      autoplay
      loop
      muted
      class="absolute bottom-4 right-4 w-40 opacity-30 pointer-events-none hidden md:block"
    >
      <!-- <source src="/waveform.mp4" type="video/mp4" /> -->
    </video>
  </div>
</template>

<script>
export default {
  name: 'AudioToText',
  data() {
    return {
      link: '',
      file: null,
      loading: false,
      transcription: '',
    };
  },
  methods: {
    handleFile(event) {
      this.file = event.target.files[0];
    },
    async startTranscription() {
      this.loading = true;
      this.transcription = '';

      const formData = new FormData();
      if (this.file) {
        formData.append('audio', this.file);
      } else if (this.link) {
        formData.append('link', this.link);
      }

      try {
        const response = await fetch('/api/transcribe', {
          method: 'POST',
          body: formData,
        });
        const result = await response.json();
        this.transcription = result.text || 'No se pudo transcribir el audio.';
      } catch (err) {
        console.error(err);
        this.transcription = 'Ocurrió un error al transcribir.';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
@keyframes fade-in {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fade-in 0.8s ease-out forwards;
}

@keyframes slide-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-slide-in {
  animation: slide-in 1s ease-out forwards;
}
</style>
