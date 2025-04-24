import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import ('@/views/HomeView.vue'),
    meta: {requiresAuth: true}
  },
  {
    path: '/expenses',
    name: 'expenses',
    component: () => import ('@/views/ExpensesView.vue'),
    meta: {requiresAuth: true}
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import ('@/views/ProfileView.vue'),
    meta: {requiresAuth: true}
  },
  {
    path: '/login',
    name: 'login',
    component: () => import ('@/views/LoginView.vue'),
    meta: {requiresGuest: true}
  },
  {
    path: '/register',
    name: 'register',
    component: () => import ('@/views/RegisterView.vue'),
    meta: {requiresGuest: true}
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore()

    if (to.meta.requiresAuth && !authStore.token) {
      next('/login')
    } else if (to.meta.requiresGuest && authStore.token) {
      next('/')
    } else {
      next()
    }
  })

export default router