import api from './index'

export const UnitsAPI = {
    async getUnits() {
        return api.get('/units/')
    },
    async createUnit(name, default_value) {
        return api.post('/units/', { name, default_value })
    },
    async updateUnit(id, name, default_value) {
        return api.patch(`/units/${id}`, { name, default_value })
    },
    async deleteUnit(id) {
        return api.delete(`/units/${id}`)
    }
}
