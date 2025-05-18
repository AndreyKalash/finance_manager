import api from "./index";

export const TagsAPI = {
  async getTags() {
    return api.get("/tags/");
  },
  async createTag(name, color) {
    return api.post("/tags/", { name, color });
  },
  async updateTag(id, name, color) {
    return api.patch(`/tags/${id}`, { name, color });
  },
  async deleteTag(id) {
    return api.delete(`/tags/${id}`);
  },
};
