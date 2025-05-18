import api from "./index";

export const RecordsAPI = {
  async getRecords(limit, skip) {
    return api.get("/records/", { limit, skip });
  },
  async createRecord(record) {
    return api.post("/records/", { ...record });
  },
  async updateRecord(record) {
    return api.patch(`/records/${record.id}`, { ...record });
  },
  async deleteRecord(id) {
    return api.delete(`/records/${id}`);
  },
};
