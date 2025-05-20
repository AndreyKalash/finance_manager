import { pathBilder } from "@/utils/api";
import api from "./index";

const path = "/records/"
const expensePath = "expense_records/"
const incomePath = "income_records/"

export const RecordsAPI = {
  async getRecords(type, limit, skip) {
    const fullPath = pathBilder(type, path, expensePath, incomePath);
    return api.get(fullPath, { limit, skip });
  },
  async createRecord(type, record) {
    const fullPath = pathBilder(type, path, expensePath, incomePath);
    return api.post(fullPath, { ...record });
  },
  async updateRecord(type, record) {
    const fullPath = pathBilder(type, path, expensePath, incomePath);
    return api.patch(fullPath + record.id, { ...record });
  },
  async deleteRecord(type, id) {
    const fullPath = pathBilder(type, path, expensePath, incomePath);
    return api.delete(fullPath + id);
  },
};
