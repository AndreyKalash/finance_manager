import { defineStore } from "pinia";
import { TagsAPI } from "@/api/tags";

export const useTagsStore = defineStore("tags", {
  state: () => ({
    tags: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchTags() {
      this.loading = true;
      this.error = null;
      try {
        const response = await TagsAPI.getTags();
        this.tags = response.data;
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка загрузки тега";
      } finally {
        this.loading = false;
      }
    },

    async createTag(payload) {
      this.error = null;
      try {
        await TagsAPI.createTag(payload);
        await this.fetchTags();
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка создания тега";
      }
    },

    async updateTag(id, name, categoryId) {
      this.error = null;
      try {
        await TagsAPI.updateTag(id, name, categoryId);
        await this.fetchTags();
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка обновления тега";
      }
    },

    async deleteTag(id) {
      this.error = null;
      try {
        await TagsAPI.deleteTag(id);
        await this.fetchTags();
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Ошибка удаления тега";
      }
    },
  },
});
