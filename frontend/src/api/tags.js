import api from "./index";
import { pathBilder } from "@/utils/api";

const path = "/tags/"
const expensePath = "expense_tags/"
const incomePath = "income_tags/"


export const TagsAPI = {
  async getTags(type) {
    const fullPath = pathBilder(type, path, expensePath, incomePath);
    return api.get(fullPath);
  },
  async createTag(type, tag) {
    const fullPath = pathBilder(type, path, expensePath, incomePath);
    return api.post(fullPath, { ...tag });
  },
  async updateTag(type, tag) {
    const fullPath = pathBilder(type, path, expensePath, incomePath);
    return api.patch(fullPath + tag.id, { name: tag.name, color: tag.color });
  },
  async deleteTag(type, id) {
    const fullPath = pathBilder(type, path, expensePath, incomePath);
    return api.delete(fullPath + id);
  },
};
