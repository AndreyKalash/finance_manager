<template>
  <div id="app">
    <header class="header container">
      <h1 class="title primary">
        <router-link to="/" class="title primary">Finance Manager</router-link>
      </h1>
      <div class="profile">
        <router-link to="/profile">
          <!-- <img src="./assets/profile.png" alt="" srcset="" class="primary"> -->
        </router-link>
      </div>
    </header>
    
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
/* Стили уже подключены в main.js */
</style>