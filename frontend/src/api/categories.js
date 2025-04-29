import api from './index'

export const CategoriesService = {
    async getCategories () {
        api.get('/categories')
    },
    async createCategory (name) {
        api.post('/categories', { name })  
    },
    async updateCategory (id, name) {
        api.put(`/categories/${id}`, { name })
    }, 
    async deleteCategory (id) {
        api.delete(`/categories/${id}`)
    },
    
    async getSubcategories () {
        api.get('/subcategories')
    },
    async createSubcategory (name, categoryId) {
        api.post('/subcategories', { name, category_id: categoryId })
    },
    async updateSubcategory (id, name, categoryId) {
        api.put(`/subcategories/${id}`, { name, category_id: categoryId })
    },
    async deleteSubcategory (id) {
        api.delete(`/subcategories/${id}`)
    }
}
