import api from './index'

export const UnitsAPI = {
    async getUnits () {
        api.get('/units/')
    },
    async createUnit (name, categoryId) {
        api.post('/units/', { name, category_id: categoryId })
    },
    async updateUnit (id, name, categoryId) {
        api.put(`/units/${id}`, { name, category_id: categoryId })
    },
    async deleteUnit (id) {
        api.delete(`/units/${id}`)
    }
}
