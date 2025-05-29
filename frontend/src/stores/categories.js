import { defineStore } from "pinia";
import { CategoriesAPI } from "@/api/categories";
import { RTYPES } from "@/utils/recordTypes";

export const useCategoriesStore = defineStore("categories", {
  state: () => ({
    categories: {
      [RTYPES.expense]: [],
      [RTYPES.income]: [],
    },
    loading: false,
    error: null,
  }),

  actions: {
    async fetchCategories(force = false) {
      this.loading = true;
      this.error = null;
      try {
        if (force || this.categories[RTYPES.expense].length == 0) {
          const expenseResponse = await CategoriesAPI.getCategories(
            RTYPES.expense
          );
          this.categories[RTYPES.expense] = expenseResponse.data;
        }
        if (force || this.categories[RTYPES.income].length == 0) {
          const incomeResponse = await CategoriesAPI.getCategories(
            RTYPES.income
          );
          this.categories[RTYPES.income] = incomeResponse.data;
        }
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка загрузки категорий";
      } finally {
        this.loading = false;
      }
    },

    async createCategory(type, category) {
      this.error = null;
      try {
        const { data } = await CategoriesAPI.createCategory(type, category);
        this.categories[type].push(data);
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка создания категории";
      }
    },

    async updateCategory(type, category) {
      this.error = null;
      try {
        const { data } = await CategoriesAPI.updateCategory(type, category);
        const idx = this.categories[type].findIndex(
          (c) => c.id === category.id
        );
        if (idx !== -1) {
          this.categories[type][idx] = {
            ...this.categories[type][idx],
            ...data,
          };
        }
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка обновления категории";
      }
    },

    async deleteCategory(type, id) {
      this.error = null;
      try {
        await CategoriesAPI.deleteCategory(type, id);
        this.categories[type] = this.categories[type].filter(
          (c) => c.id !== id
        );
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка удаления категории";
      }
    },
  },
});
