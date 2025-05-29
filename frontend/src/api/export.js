import api from "@/api";

export const FilesAPI = {
  async getExportRecords(type, extension) {
    return api.get(`/export/${type}/`, {
      params: { extension },
    });
  },
};
