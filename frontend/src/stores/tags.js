import { defineStore } from "pinia";
import { TagsAPI } from "@/api/tags";
import { RTYPES } from "@/utils/recordTypes";

export const useTagsStore = defineStore("tags", {
  state: () => ({
    tags: {
      [RTYPES.expense]: [],
      [RTYPES.income]: [],
    },
    loading: false,
    error: null,
  }),
  actions: {
    async fetchTags(force = false) {
      this.loading = true;
      this.error = null;
      try {
        if (force || this.tags[RTYPES.expense].length == 0) {
          const expenseResponse = await TagsAPI.getTags(RTYPES.expense);
          this.tags[RTYPES.expense] = expenseResponse.data;
        }
        if (force || this.tags[RTYPES.income].length == 0) {
          const incomeResponse = await TagsAPI.getTags(RTYPES.income);
          this.tags[RTYPES.income] = incomeResponse.data;
        }
      } catch (error) {
        this.error = error.response?.data?.detail || "Ошибка загрузки тегов";
      } finally {
        this.loading = false;
      }
    },

    async createTag(type, tag) {
      this.error = null;
      try {
        const { data } = await TagsAPI.createTag(type, tag);
        this.tags[type].push(data);
      } catch (error) {
        this.error = error.response?.data?.detail || "Ошибка создания тега";
      }
    },

    async updateTag(type, tag) {
      this.error = null;
      try {
        const { data } = await TagsAPI.updateTag(type, tag);
        const idx = this.tags[type].findIndex((t) => t.id === tag.id);
        if (idx !== -1) {
          this.tags[type][idx] = { ...this.tags[type][idx], ...data };
        }
      } catch (error) {
        this.error = error.response?.data?.detail || "Ошибка обновления тега";
      }
    },

    async deleteTag(type, id) {
      this.error = null;
      try {
        await TagsAPI.deleteTag(type, id);
        this.tags[type] = this.tags[type].filter((t) => t.id !== id);
      } catch (error) {
        this.error = error.response?.data?.detail || "Ошибка удаления тега";
      }
    },
  },
});
