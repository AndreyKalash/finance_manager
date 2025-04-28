import { useAuthStore } from "@/stores/auth";

export function authGuard(to, from, next) {
    const authStore = useAuthStore();
    
    if (to.meta.requiresAuth && !authStore.user) {
      authStore.redirectPath = to.fullPath;
      next('/login');
    } else {
      next();
    }
  }
  