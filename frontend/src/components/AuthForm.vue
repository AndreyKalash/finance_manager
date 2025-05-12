<template>
  <section class="auth_section">
    <div class="container">
      <div class="auth_content">
        <p class="title primary">{{ isLoginMode ? 'Вход' : 'Регистрация' }}</p>
        <form @submit.prevent="handleSubmit">
          <input v-model="formData.email" type="email" placeholder="Электронная почта" required>
          <input v-if="!isLoginMode" v-model="formData.username" type="text" placeholder="Логин" required>
          <input v-model="formData.password" type="password" placeholder="Пароль" required>
          <input v-if="!isLoginMode" v-model="formData.confirmPassword" type="password" placeholder="Повторите пароль"
            required>
          <button type="submit">{{ isLoginMode ? 'Войти' : 'Зарегистрироваться' }}</button>
        </form>
        <div class="form_switch">
          <p>{{ isLoginMode ? 'Нет аккаунта?' : 'Уже есть аккаунт?' }}</p>
          <router-link :to="isLoginMode ? '/register' : '/login'" class="switch-link" active-class="active"
            exact-active-class="exact-active">
            {{ isLoginMode ? 'Зарегистрироваться' : 'Войти' }}
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>

import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const isLoginMode = computed(() => route.path === '/login')
const errorMessage = ref('')
const authStore = useAuthStore()

const formData = ref({
  email: '',
  username: '',
  password: '',
  confirmPassword: ''
})

const handleSubmit = async () => {
  if (isLoginMode.value) {
    await handleLogin()
  } else {
    await handleRegister()
  }
}

const handleLogin = async () => {
  try {
    errorMessage.value = ''

    await authStore.login({
      username: formData.value.email,
      password: formData.value.password
    });

    const redirectPath = authStore.redirectPath || '/';
    router.push(redirectPath);

  } catch (error) {
    errorMessage.value = 'Неверный email или пароль'
    console.error('Login failed:', error)
  }
}

const handleRegister = async () => {
  if (formData.value.password !== formData.value.confirmPassword) {
    errorMessage.value = 'Пароли не совпадают';
    return;
  }
  try {
    errorMessage.value = '';
    
    await authStore.register({
      email: formData.value.email,
      username: formData.value.username,
      password: formData.value.password
    });
    await handleLogin()
    
  } catch (error) {
    errorMessage.value = error.toString();
    console.error('Registration failed:', error);
  }
};
</script>

<style scoped>
form {
  width: 400px;
  display: flex;
  flex-direction: column;
}

.auth_section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.container {
  width: 100%;
  max-width: 500px;
}

.auth_content {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

.title {
  text-align: center;
  margin-bottom: 20px;
}

input {
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  color: black;
  font-size: 16px;
  width: 95%;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: 10px !important;
  border-color: #bb86fc !important;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 15px;
}

button:hover {
  border: 5px;
  border-color: #bb86fc;
}

.form_switch {
  margin-bottom: 15px;
  text-align: center;
}

a {
  cursor: pointer;
  text-decoration: underline;
}

a:hover {
  color: #42b983;
}

.switch-link {
  color: inherit;
  text-decoration: underline;
  cursor: pointer;
  transition: color 0.3s;
}

.switch-link:hover {
  color: #42b983;
}

.switch-link.active,
.switch-link.exact-active {
  color: #42b983;
  font-weight: 500;
  text-decoration: none;
}
</style>