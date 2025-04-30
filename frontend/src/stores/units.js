import { defineStore } from "pinia";
import { UnitsAPI } from "@/api/units";

export const useUnitsStore = defineStore("units", {
  state: () => ({
    units: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchUnits() {
      this.loading = true;
      this.error = null;
      try {
        const response = await UnitsAPI.getUnits();
        this.units = response.data;
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка загрузки категорий";
      } finally {
        this.loading = false;
      }
    },

    async createUnit(payload) {
      this.error = null;
      try {
        await UnitsAPI.createUnit(payload);
        await this.fetchUnits();
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка создания единицы измерения";
      }
    },

    async updateUnit(id, name) {
      this.error = null;
      try {
        await UnitsAPI.updateUnit(id, name);
        await this.fetchUnits();
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка обновления единицы измерения";
      }
    },

    async deleteUnit(id) {
      this.error = null;
      try {
        await UnitsAPI.deleteUnit(id);
        await this.fetchUnits();
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка удаления единицы измерения";
      }
    },
}
});
