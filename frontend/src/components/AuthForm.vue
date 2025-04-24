<template>
    <section class="auth_section">
      <div class="container">
            <div class="auth_content">
                <p class="title primary">{{ isLoginMode ? 'Вход' : 'Регистрация' }}</p>
                <form @submit="handleSubmit">
                <input v-if="!isLoginMode"
                    v-model="formData.email" 
                    type="email" 
                    placeholder="Электронная почта"
                    required
                >
                <input v-if="isLoginMode"
                    v-model="formData.username" 
                    type="username" 
                    placeholder="Логин"
                    required
                >
                <input 
                    v-model="formData.password" 
                    type="password" 
                    placeholder="Пароль"
                    required
                >
                <input v-if="!isLoginMode"
                    v-model="formData.sumbitPassword" 
                    type="password" 
                    placeholder="Повторите пароль"
                    required
                >
                <button type="submit">{{ isLoginMode ? 'Войти' : 'Зарегистрироваться' }}</button>
                </form>
                <div class="form_switch">
                    <p>{{ isLoginMode ? 'Нет аккаунта?' : 'Уже есть аккаунт?' }}</p>
                    <a @click="toggleMode">
                    {{ isLoginMode ? 'Зарегистрироваться' : 'Войти' }}
                    </a>
                </div>
            </div>
        </div>
    </section>
</template>
  
<script setup>

import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { api } from '@/api/index'

const props = defineProps({
  mode: {
    type: String,
    default: 'login',
    validator: value => ['login', 'register'].includes(value)
  }
})

const router = useRouter()
const currentMode = ref(props.mode)
const isLoginMode = computed(() => currentMode.value === 'login')
const errorMessage = ref('')
const authStore = useAuthStore()

const formData = ref({
  email: '',
  password: '',
  confirmPassword: ''
})

const toggleMode = () => {
  currentMode.value = isLoginMode.value ? 'register' : 'login'
  formData.value = { email: '', password: '', confirmPassword: '' }
  errorMessage.value = ''
}

const handleSubmit = async () => {
    console.log('1' + String(isLoginMode.value));
    console.log('2' + currentMode.value);
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
      username: formData.value.username,
      password: formData.value.password
    })
    router.push('/')
  } catch (error) {
    errorMessage.value = 'Неверный email или пароль'
    console.error('Login failed:', error)
  }
}

const handleRegister = async () => {
  if (formData.value.password !== formData.value.confirmPassword) {
    errorMessage.value = 'Пароли не совпадают'
    return
  }
  try {
    errorMessage.value = ''
    const response = await api.post('/auth/register', {
      email: formData.value.email,
      password: formData.value.password,
      username: formData.value.username
    });
    console.log(response)
    await handleLogin();
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Ошибка регистрации'
    console.error('Registration failed:', error)
  }
}

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
</style>