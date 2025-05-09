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
        this.units = response.data?.items || response.data || [];
      } catch (error) {
        this.error = error.response?.data?.detail || "Ошибка загрузки тегов";
        console.error("API Error:", error.response?.data);
      } finally {
        this.loading = false;
      }
    },

    async createUnit(name, defaultValue) {
      
      this.error = null;
      try {
        const { data } = await UnitsAPI.createUnit(name, defaultValue);
        this.units.push(data)
      } catch (error) {
        this.error =
        error.response?.data?.detail || "Ошибка создания единицы измерения";
      }
    },
    
    async updateUnit(id, name, default_value) {
      this.error = null;
      try {
        const { data } = await UnitsAPI.updateUnit(id, name, default_value);
        const idx = this.units.findIndex((u) => u.id === id);
        if (idx !== -1) {
          this.units[idx] = { ...this.units[idx], ...data };
        }
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка обновления единицы измерения";
      }
    },

    async deleteUnit(id) {
      this.error = null;
      try {
        await UnitsAPI.deleteUnit(id);
        this.units = this.units.filter((u) => u.id !== id);
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка удаления единицы измерения";
      }
    },
}
});
