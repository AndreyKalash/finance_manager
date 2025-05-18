import { useAuthStore } from "@/stores/auth";

export async function authGuard(to, from, next) {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth) {
    if (authStore.token && !authStore.user) {
      try {
        await authStore.fetchUser();
      } catch (error) {
        authStore.logout();
        return next("/login");
      }
    }

    if (!authStore.user) {
      authStore.redirectPath = to.fullPath;
      return next("/login");
    }
  }

  next();
}
