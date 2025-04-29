<template>
  <header class="header container">
    <h1 class="title primary">Finance Manager</h1>
    <div v-if="authStore.user" class="header-right">
      <div class="logout-dropdown">
        <button class="logout-btn" @click="toggleDropdown">
          <svg class="profile-icon" viewBox="0 0 24 24">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
          </svg>
        </button>
        <ul v-if="showDropdown" class="dropdown-menu">
              <li><router-link to="/me">Профиль</router-link></li>
              <li @click="handleLogout">Выйти</li>
            </ul>
          </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();
const showDropdown = ref(false);

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
};

const handleLogout = async () => {
  await authStore.logout();
  router.push('/login');
};

document.addEventListener('click', (e) => {
  if (!e.target.closest('.logout-dropdown')) {
    showDropdown.value = false;
  }
});
</script>

<style scoped>
.header {
  display: flex;
  justify-content: center;
  align-items: center;
}

.header .title {
  flex-grow: 1;
  text-align: center;
}

.header-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.profile {
  margin-right: 20px;
}

.profile-icon {
  width: 32px;
  height: 32px;
  fill: #666;
  cursor: pointer;
  transition: fill 0.2s;
}

.profile-icon:hover {
  fill: #42b983;
}

.logout-dropdown {
  position: relative;
}

.logout-btn {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
}

.logout-icon {
  width: 32px;
  height: 32px;
  fill: #666;
  transition: fill 0.2s;
}

.logout-icon:hover {
  fill: #42b983;
}

.dropdown-menu {
  position: absolute;
  top: 40px;
  right: 0;
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.dropdown-menu li {
  padding: 5px;
  border-bottom: 1px solid #ddd;
}

.dropdown-menu li:last-child {
  border-bottom: none;
}

.dropdown-menu li a, .dropdown-menu li {
  text-decoration: none;
  color: #666;
  transition: color 0.2s;
}

.dropdown-menu li a:hover, .dropdown-menu li:hover {
  color: #42b983;
}
</style>
