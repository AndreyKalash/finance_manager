import api from "@/api";

export const StatsAPI = {
  async getCategoriesMonthSum(month, year) {
    return api.get("/stats/categories-month-sum", {
      params: { month, year },
    });
  },

  async getCategoriesMonthCount(month, year) {
    return api.get("/stats/categories-month-count", {
      params: { month, year },
    });
  },
};
