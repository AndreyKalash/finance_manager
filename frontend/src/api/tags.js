import api from './index'

export const TagsAPI = {
    async getTags () {
        api.get('/tags/')
    },
    async createTag (name, categoryId) {
        api.post('/tags/', { name, category_id: categoryId })
    },
    async updateTag (id, name, categoryId) {
        api.put(`/tags/${id}`, { name, category_id: categoryId })
    },
    async deleteTag (id) {
        api.delete(`/tags/${id}`)
    }
}
