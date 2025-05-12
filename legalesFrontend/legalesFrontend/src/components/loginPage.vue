<template>
  <div class="login-container">
    <div class="carousel-section">
      <div class="carousel">
        <transition-group name="fade" tag="div">
          <img :src="images[currentImage]" :key="currentImage" alt="Slide" />
        </transition-group>
      </div>
    </div>

    <div class="form-section">
      <h1>Bienvenido</h1>
      <p>Accedé al panel de control</p>
      <form @submit.prevent="handleLogin">
        <input type="text" placeholder="Usuario" v-model="username" required />
        <input type="password" placeholder="Contraseña" v-model="password" required />
        <button type="submit">Ingresar</button>
      </form>
    </div>
  </div>
</template>

<script>
import slide1 from '@/assets/meeting1.png'
import slide2 from '@/assets/support3a.png'
import slide3 from '@/assets/training2a.png'

export default {
  name: 'LoginPage',
  emits: ['login-exitoso'], // 👈 AÑADIDO: para emitir evento
  data() {
    return {
      username: '',
      password: '',
      images: [slide1, slide2, slide3],
      currentImage: 0,
    };
  },
  mounted() {
    setInterval(() => {
      this.currentImage = (this.currentImage + 1) % this.images.length;
    }, 6000);
  },
  methods: {
    handleLogin() {
      console.log('Usuario:', this.username);
      console.log('Contraseña:', this.password);

      // 👇 Validación de ejemplo (podés reemplazarla por una real)
      if (this.username === 'admin' && this.password === '1234') {
        this.$emit('login-exitoso'); // 👈 EVENTO HACIA App.vue
      } else {
        alert('Usuario o contraseña incorrectos');
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, #0077ff, #9b59b6, #6a0572);
  color: #fff;
  font-family: 'Segoe UI', sans-serif;
}

.carousel-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.carousel img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  transition: opacity 0.8s ease-in-out;
}

.form-section {
  flex: 1;
  background: rgba(255, 255, 255, 0.1);
  padding: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  backdrop-filter: blur(10px);
}

.form-section h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.form-section p {
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

form input {
  width: 100%;
  padding: 0.8rem;
  margin-bottom: 1rem;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
}

form button {
  padding: 0.8rem;
  width: 100%;
  background-color: #ffffffcc;
  color: #000;
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
}

form button:hover {
  background-color: #fff;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 1s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
