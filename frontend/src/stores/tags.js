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
        this.tags = response.data?.items || response.data || [];
      } catch (error) {
        this.error = error.response?.data?.detail || "Ошибка загрузки тегов";
      } finally {
        this.loading = false;
      }
    },

    async createTag(name, color) {
      this.error = null;
      try {
        const { data } = await TagsAPI.createTag(name, color);
        this.tags.push(data);
      } catch (error) {
        this.error = error.response?.data?.detail || "Ошибка создания тега";
      }
    },

    async updateTag({ id, name, color }) {
      this.error = null;
      try {
        const { data } = await TagsAPI.updateTag(id, name, color);
        const idx = this.tags.findIndex((t) => t.id === id);
        if (idx !== -1) {
          this.tags[idx] = { ...this.tags[idx], ...data };
        }
      } catch (error) {
        this.error = error.response?.data?.detail || "Ошибка обновления тега";
      }
    },

    async deleteTag(id) {
      this.error = null;
      try {
        await TagsAPI.deleteTag(id);
        this.tags = this.tags.filter((t) => t.id !== id);
      } catch (error) {
        this.error = error.response?.data?.detail || "Ошибка удаления тега";
      }
    },
  },
});
