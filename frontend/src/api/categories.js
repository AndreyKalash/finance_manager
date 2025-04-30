import api from './index'

export const CategoriesAPI = {
    async getCategories () {
        return api.get('/categories/')
    },
    async createCategory (category_name, category_color) {
        return api.post('/categories/', {category_name, category_color})  
    },
    async updateCategory (id, name) {
        return api.put(`/categories/${id}`, { name })
    }, 
    async deleteCategory (id) {
        return api.delete(`/categories/${id}`)
    }
}
