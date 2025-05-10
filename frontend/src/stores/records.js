import { defineStore } from "pinia";
import { RecordsAPI } from "@/api/records";

export const useRecordsStore = defineStore("records", {
  state: () => ({
    records: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchRecords(limit=50, skip=0) {
      this.loading = true;
      this.error = null;
      try {
        const response = await RecordsAPI.getRecords(limit, skip);
        this.records = response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || "Ошибка загрузки записей";
      } finally {
        this.loading = false;
      }
    },
    async createRecord(record) {
      this.error = null;
      try {
        const { data } = await RecordsAPI.createRecord(record);
        this.records.push(data);
      } catch (error) {
        this.error = error.response?.data?.detail || "Ошибка создания записи";
      }
    },
    async updateRecord(record) {
      this.error = null;
      try {
        const { data } = await RecordsAPI.updateRecord(record);
        const idx = this.records.findIndex((r) => r.id === record.id);
        if (idx !== -1) {
          this.records[idx] = { ...this.records[idx], ...data };
        }
      } catch (error) {
        this.error = error.response?.data?.detail || "Ошибка обновления записи";
      }
    },
    async deleteRecord(id) {
      this.error = null;
      try {
        await RecordsAPI.deleteRecord(id);
        this.records = this.records.filter((r) => r.id !== id);
      } catch (error) {
        this.error = error.response?.data?.detail || "Ошибка удаления записи";
      }
    },
  },
});
