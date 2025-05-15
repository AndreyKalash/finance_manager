import api from './index'

export const CategoriesAPI = {
    async getCategories() {
        return api.get('/categories/')
    },
    async createCategory(name, color) {
        return api.post('/categories/', {name, color})  
    },
    async updateCategory(id, name, color) {
        return api.patch(`/categories/${id}`, { name, color })
    }, 
    async deleteCategory(id) {
        return api.delete(`/categories/${id}`)
    }
}
