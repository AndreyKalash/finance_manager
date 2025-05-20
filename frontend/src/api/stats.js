import api from "@/api";

export const StatsAPI = {
  async getCategoriesMonthSum(type, month, year) {
    return api.get(`/stats/${type}/categories-month-sum`, {
      params: { month, year },
    });
  },

  async getCategoriesMonthCount(type, month, year) {
    return api.get(`/stats/${type}/categories-month-count`, {
      params: { month, year },
    });
  },
};
