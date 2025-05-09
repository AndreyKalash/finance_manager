import api from './index'

export const RecordsAPI = {
    async getRecords() {
        return api.get('/records/')
    },
    async createRecord(record) {
        return api.post('/records/', {...record})  
    },
    async updateRecord(id, name, color) {
        return api.patch(`/records/${id}/`, { name, color })
    }, 
    async deleteRecord(id) {
        return api.delete(`/records/${id}`)
    }
}
