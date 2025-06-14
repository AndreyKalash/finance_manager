<template>
  
  <div id="app">
    <AppHeader />
    <router-view />
  </div>
</template>

<script>
import AppHeader from '@/components/layout/AppHeader.vue';
document.title = 'Finance Manager'
export default {
  name: 'App',
  components: {
    AppHeader
  }
}
</script>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
