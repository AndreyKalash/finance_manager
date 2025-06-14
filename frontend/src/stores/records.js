import { defineStore } from "pinia";
import { RecordsAPI } from "@/api/records";
import { RTYPES } from "@/utils/recordTypes";

export const useRecordsStore = defineStore("records", {
  state: () => ({
    records: {
      [RTYPES.expense]: [],
      [RTYPES.income]: [],
    },
    loading: false,
    error: null,
  }),
  getters: {
    hasRecords: (state) =>
      state.records[RTYPES.expense].length > 0 &&
      state.records[RTYPES.income].length > 0,
  },

  actions: {
    async fetchRecords(limit = 50, skip = 0, force = false) {
      if (!force && this.hasRecords) return;
      await this.fetchIncomeRecords(limit, skip, force);
      await this.fetchExpenseRecords(limit, skip, force);
    },
    async fetchTypedRecords(limit = 50, skip = 0, force = false, type) {
      if (type == RTYPES.income) {
        await this.fetchIncomeRecords(limit, skip, force);
      } else if (type == RTYPES.expense) {
        await this.fetchExpenseRecords(limit, skip, force);
      }
    },
    async fetchIncomeRecords(limit = 50, skip = 0, force = false) {
      if (!force && this.hasRecords) return;
      this.loading = true;
      this.error = null;
      try {
        if (force || this.records[RTYPES.income].length == 0) {
          const incomeResponse = await RecordsAPI.getRecords(
            RTYPES.income,
            limit,
            skip
          );
          this.records[RTYPES.income].push(...incomeResponse.data);
        }
      } catch (error) {
        this.error = error.response?.data?.detail || "Ошибка загрузки записей";
      } finally {
        this.loading = false;
      }
    },
    async fetchExpenseRecords(limit = 50, skip = 0, force = false) {
      if (!force && this.hasRecords) return;
      this.loading = true;
      this.error = null;
      try {
        if (force || this.records[RTYPES.expense].length == 0) {
          const expenseResponse = await RecordsAPI.getRecords(
            RTYPES.expense,
            limit,
            skip
          );
          this.records[RTYPES.expense].push(...expenseResponse.data);
        }
      } catch (error) {
        this.error = error.response?.data?.detail || "Ошибка загрузки записей";
      } finally {
        this.loading = false;
      }
    },
    async createRecord(type, record) {
      this.error = null;
      try {
        const { data } = await RecordsAPI.createRecord(type, record);
        this.records[type].push(data);
      } catch (error) {
        this.error = error.response?.data?.detail || "Ошибка создания записи";
      }
    },
    async updateRecord(type, record) {
      this.error = null;
      try {
        const { data } = await RecordsAPI.updateRecord(type, record);
        const idx = this.records[type].findIndex((r) => r.id === record.id);
        if (idx !== -1) {
          this.records[type][idx] = { ...this.records[type][idx], ...data };
        }
      } catch (error) {
        this.error = error.response?.data?.detail || "Ошибка обновления записи";
      }
    },
    async deleteRecord(type, id) {
      this.error = null;
      try {
        await RecordsAPI.deleteRecord(type, id);
        this.records[type] = this.records[type].filter((r) => r.id !== id);
      } catch (error) {
        this.error = error.response?.data?.detail || "Ошибка удаления записи";
      }
    },
    async exportRecords(type, extension) {
      this.error = null;
      try {
        const response = await RecordsAPI.exportRecords(type, extension);

        const blob = new Blob([response.data], {
          type: response.headers["content-type"],
        });
        const url = window.URL.createObjectURL(blob);

        const contentDisposition = response.headers["content-disposition"];
        const fileNameMatch = contentDisposition.match(
          /filename="?(.+?)"?(;|$)/
        );
        const fileName = fileNameMatch ? fileNameMatch[1] : `data.${extension}`;

        const link = document.createElement("a");
        link.href = url;
        link.download = fileName;
        document.body.appendChild(link);
        link.click();

        window.URL.revokeObjectURL(url);
        document.body.removeChild(link);
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка при экспорте данных";
      }
    },
  },
});
