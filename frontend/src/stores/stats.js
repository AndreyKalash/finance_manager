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
    async fetchStats(month, year) {
      this.setChartPeriod(month, year);
      console.log(this.currentChartMonth, this.currentChartYear)
      await this.fetchCategoriesMonthSum(month, year);
      await this.fetchCategoriesMonthCount(month, year);
    },
    setChartPeriod(month, year) {
      this.currentChartMonth = month;
      this.currentChartYear = year;
    },
    async fetchCategoriesMonthSum(month, year) {
      this.loading = true;
      this.error = null;
      try {
        const response = await StatsAPI.getCategoriesMonthSum(month, year);
        this.categoriesMonthSum = response.data;
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка загрузки статистики";
      } finally {
        this.loading = false;
      }
    },

    async fetchCategoriesMonthCount(month, year) {
      this.loading = true;
      this.error = null;
      try {
        const response = await StatsAPI.getCategoriesMonthCount(month, year);
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
