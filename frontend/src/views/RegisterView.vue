<template>
    <AuthForm mode="register"/>
</template>

<script setup>
import AuthForm from '@/components/AuthForm.vue'
</script>

<style scoped>
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
</style>