<!-- AuthForm.vue -->
<template>
  <section class="auth_section">
    <div class="container">
      <div class="auth_content">
        <!-- Динамическое изменение заголовка в зависимости от режима -->
        <p class="title primary">{{ isLoginMode ? "Вход" : "Регистрация" }}</p>
        <!-- Предотвращение стандартной отправки формы и вызов кастомного обработчика -->
        <form @submit.prevent="handleSubmit">
          <input
            v-model="formData.email"
            type="email"
            placeholder="Электронная почта"
            required
            @input="clearError('email')"
            />
          <span class="error">{{ errors.email }}</span>
          <!-- Условный рендеринг поля username только для регистрации -->
          <input
            v-if="!isLoginMode"
            v-model="formData.username"
            type="text"
            placeholder="Логин"
            required
            @input="clearError('username')"
          />
          <span class="error">{{ errors.username }}</span>
          <input
            v-model="formData.password"
            type="password"
            placeholder="Пароль"
            required
            @input="clearError('password')"
          />
          <span class="error">{{ errors.password }}</span>
          <!-- Поле подтверждения пароля отображается только при регистрации -->
          <input
            v-if="!isLoginMode"
            v-model="formData.confirmPassword"
            type="password"
            placeholder="Повторите пароль"
            required
            @input="clearError('confirmPassword')"
          />
          <span class="error">{{ errors.confirmPassword }}</span>
          <!-- Динамический текст кнопки в зависимости от режима -->
          <button type="submit">
            {{ isLoginMode ? "Войти" : "Зарегистрироваться" }}
          </button>
        </form>
        <div class="form_switch">
          <p>{{ isLoginMode ? "Нет аккаунта?" : "Уже есть аккаунт?" }}</p>
          <!-- Динамическая маршрутизация с изменением пути в зависимости от текущего режима -->
          <router-link
            :to="isLoginMode ? '/register' : '/login'"
            class="switch-link"
            active-class="active"
            exact-active-class="exact-active"
          >
            {{ isLoginMode ? "Зарегистрироваться" : "Войти" }}
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const route = useRoute();
// Вычисляемое свойство для определения режима компонента на основе текущего маршрута
const isLoginMode = computed(() => route.path === "/login");
const errorMessage = ref("");
const authStore = useAuthStore();
// Реактивные данные формы с инициализацией пустыми значениями
const formData = ref({
  email: "",
  username: "",
  password: "",
  confirmPassword: "",
});
// Отдельный объект для хранения ошибок валидации каждого поля
const errors = ref({
  email: "",
  username: "",
  password: "",
  confirmPassword: "",
});
// Валидация email с использованием регулярного выражения
const validateEmail = () => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!formData.value.email) {
    errors.value.email = "Email обязателен";
    return false;
  }
  if (!emailRegex.test(formData.value.email)) {
    errors.value.email = "Некорректный формат email";
    return false;
  }
  errors.value.email = "";
  return true;
};
// Валидация пароля
const validatePassword = () => {
  if (!formData.value.password) {
    errors.value.password = "Пароль обязателен";
    return false;
  }
  if (formData.value.password.length < 6) {
    errors.value.password = "Пароль должен быть не менее 6 символов";
    return false;
  }
  errors.value.password = "";
  return true;
};
// Условная валидация username только для режима регистрации
const validateUsername = () => {
  if (!isLoginMode.value) {
    if (!formData.value.username) {
      errors.value.username = "Логин обязателен";
      return false;
    }
    if (formData.value.username.length < 3) {
      errors.value.username = "Логин должен быть не менее 3 символов";
      return false;
    }
  }
  errors.value.username = "";
  return true;
};
// Валидация совпадения паролей при регистрации
const validateConfirmPassword = () => {
  if (!isLoginMode.value) {
    if (!formData.value.confirmPassword) {
      errors.value.confirmPassword = "Подтвердите пароль";
      return false;
    }
    if (formData.value.password !== formData.value.confirmPassword) {
      errors.value.confirmPassword = "Пароли не совпадают";
      return false;
    }
  }
  errors.value.confirmPassword = "";
  return true;
};
// Последовательная валидация всех полей с сохранением состояния валидности
const validateForm = () => {
  let isValid = true;
  isValid = validateEmail() && isValid;
  isValid = validatePassword() && isValid;
  if (!isLoginMode.value) {
    isValid = validateUsername() && isValid;
    isValid = validateConfirmPassword() && isValid;
  }
  
  return isValid;
};
// Утилитарная функция для очистки ошибок при взаимодействии пользователя с полями
const clearError = (field) => {
  errors.value[field] = "";
  errorMessage.value = "";
};
// Центральный обработчик отправки формы с условным выбором действия
const handleSubmit = async () => {
  if (!validateForm()) return;
  if (isLoginMode.value) {
    await handleLogin();
  } else {
    await handleRegister();
  }
};
// Обработчик входа
const handleLogin = async () => {
  try {
    errorMessage.value = "";

    await authStore.login({
      username: formData.value.email,
      password: formData.value.password,
    });

    const redirectPath = authStore.redirectPath || "/";
    router.push(redirectPath);
  } catch (error) {
    errorMessage.value = "Неверный email или пароль";
    console.error("Login failed:", error);
  }
};
// Обработчик регистрации
const handleRegister = async () => {
  if (formData.value.password !== formData.value.confirmPassword) {
    errorMessage.value = "Пароли не совпадают";
    return;
  }
  try {
    errorMessage.value = "";

    await authStore.register({
      email: formData.value.email,
      username: formData.value.username,
      password: formData.value.password,
    });
    await handleLogin();
  } catch (error) {
    errorMessage.value = error.toString();
    console.error("Registration failed:", error);
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
  margin-bottom: 1rem;
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
.error {
  color: #ff4444;
  font-size: 0.8rem;
  margin-top: 0.25rem;
  display: block;
}
</style>
