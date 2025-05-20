import api from "./index";
import { pathBilder } from "../utils/api";

const path = "/categories/"
const expensePath = "expense_categories/"
const incomePath = "income_categories/"

export const CategoriesAPI = {
  async getCategories(type) {
    const fullPath = pathBilder(type, path, expensePath, incomePath);
    return api.get(fullPath);
  },
  async createCategory(type, category) {
    const fullPath = pathBilder(type, path, expensePath, incomePath);
    return api.post(fullPath, { ...category });
  },
  async updateCategory(type, category) {
    const fullPath = pathBilder(type, path, expensePath, incomePath);
    return api.patch(fullPath + category.id, { name: category.name, color: category.color });
  },
  async deleteCategory(type, id) {
    const fullPath = pathBilder(type, path, expensePath, incomePath);
    return api.delete(fullPath + id);
  },
};
