import { defineStore } from "pinia";
import { StatsAPI } from "@/api/stats";

export const useStatsStore = defineStore("stats", {
  state: () => ({
    categoriesMonthSum: [],
    categoriesMonthCount: [],
    loading: false,
    error: null,
    currentChartMonth: null,
    currentChartYear: null,
  }),
  actions: {
    async fetchStats(type, month, year) {
      this.setChartPeriod(month, year);
      await this.fetchCategoriesMonthSum(type, month, year);
      await this.fetchCategoriesMonthCount(type, month, year);
    },
    setChartPeriod(month, year) {
      this.currentChartMonth = month;
      this.currentChartYear = year;
    },
    async fetchCategoriesMonthSum(type, month, year) {
      this.loading = true;
      this.error = null;
      try {
        const response = await StatsAPI.getCategoriesMonthSum(type, month, year);
        this.categoriesMonthSum = response.data;
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка загрузки статистики";
      } finally {
        this.loading = false;
      }
    },

    async fetchCategoriesMonthCount(type, month, year) {
      this.loading = true;
      this.error = null;
      try {
        const response = await StatsAPI.getCategoriesMonthCount(type, month, year);
        this.categoriesMonthCount = response.data;
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка загрузки статистики";
      } finally {
        this.loading = false;
      }
    },
  },
});
