import { defineStore } from "pinia";
import { CategoriesAPI } from "@/api/categories";

export const useCategoriesStore = defineStore("categories", {
  state: () => ({
    categories: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchCategories() {
      this.loading = true;
      this.error = null;
      try {
        const response = await CategoriesAPI.getCategories();
        this.categories = response.data;
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка загрузки категорий";
      } finally {
        this.loading = false;
      }
    },

    async createCategory({ categoriy_name, categoriy_color }) {
      this.error = null;
      try {
        const { data } = await CategoriesAPI.createCategory({ categoriy_name, categoriy_color });
        this.categories.push(data)
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка создания категории";
      }
    },

    async updateCategory(id, name) {
      this.error = null;
      try {
        const { data } = await CategoriesAPI.updateCategory(id, name);
        const idx = this.categories.findIndex(c => c.id === id);
        if (idx !== -1) {
            this.categories[idx] = { ...this.categories[idx], ...data };
        }
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка обновления категории";
      }
    },

    async deleteCategory(id) {
      this.error = null;
      try {
        await CategoriesAPI.deleteCategory(id);
        this.categories = this.categories.filter(c => c.id !== id)
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка удаления категории";
      }
    },
  },
});
