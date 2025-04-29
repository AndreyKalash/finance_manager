<template>
  <section class="profile">
    <AppHeader />
    <div class="container">
      <h2>Профиль пользователя</h2>
      <div v-if="user" class="profile-info">
        <p><strong>Имя пользователя:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
      </div>
    </div>
  </section>

  <section>
    <div class="settings container">
      <h2 class="title primary">Категории</h2>
      <div class="categories-section">
        <div class="category-list">
          <h3>Основные категории</h3>
          <ul>
            <li v-for="category in mainCategories" :key="category.id">
              {{ category.name }}
              <button @click="startEditCategory(category)">
                <i class="fa-solid fa-pen"></i>
              </button>
              <button @click="handleDeleteCategory(category.id)">
                <i class="fa-solid fa-trash"></i>
              </button>
            </li>
          </ul>
          <div class="add-category">
            <input v-model="newCategoryName" placeholder="Новая категория" />
            <button @click="handleAddCategory">Добавить</button>
          </div>
        </div>

        <div class="subcategory-list">
          <h3>Подкатегории</h3>
          <ul>
            <li v-for="subcategory in subcategories" :key="subcategory.id">
              {{ subcategory.name }} ({{ getCategoryName(subcategory.category_id) }})
              <button @click="startEditSubcategory(subcategory)">
                <i class="fa-solid fa-pen"></i>
              </button>
              <button @click="handleDeleteSubcategory(subcategory.id)">
                <i class="fa-solid fa-trash"></i>
              </button>
            </li>
          </ul>
          <div class="add-subcategory">
            <select v-model="newSubcategoryCategory">
              <option v-for="cat in mainCategories" :value="cat.id" :key="cat.id">
                {{ cat.name }}
              </option>
            </select>
            <input v-model="newSubcategoryName" placeholder="Новая подкатегория" />
            <button @click="handleAddSubcategory">Добавить</button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import { getMe } from '@/api/users'
import {
  getCategories, createCategory, deleteCategory,
  getSubcategories, createSubcategory, deleteSubcategory
} from '@/api/categories'

const user = ref(null)
const mainCategories = ref([])
const subcategories = ref([])

const newCategoryName = ref('')
const newSubcategoryName = ref('')
const newSubcategoryCategory = ref(null)

const fetchUser = async () => {
  const { data } = await getMe()
  user.value = data
}

const fetchCategories = async () => {
  const { data } = await getCategories()
  mainCategories.value = data
  if (data.length && !newSubcategoryCategory.value) {
    newSubcategoryCategory.value = data[0].id
  }
}

const fetchSubcategories = async () => {
  const { data } = await getSubcategories()
  subcategories.value = data
}

const handleAddCategory = async () => {
  if (!newCategoryName.value.trim()) return
  await createCategory(newCategoryName.value.trim())
  newCategoryName.value = ''
  await fetchCategories()
}

const handleDeleteCategory = async (id) => {
  if (!confirm('Удалить категорию?')) return
  await deleteCategory(id)
  await fetchCategories()
  await fetchSubcategories()
}

const handleAddSubcategory = async () => {
  if (!newSubcategoryName.value.trim() || !newSubcategoryCategory.value) return
  await createSubcategory(newSubcategoryName.value.trim(), newSubcategoryCategory.value)
  newSubcategoryName.value = ''
  await fetchSubcategories()
}

const handleDeleteSubcategory = async (id) => {
  if (!confirm('Удалить подкатегорию?')) return
  await deleteSubcategory(id)
  await fetchSubcategories()
}

const getCategoryName = (categoryId) => {
  const cat = mainCategories.value.find(c => c.id === categoryId)
  return cat ? cat.name : ''
}

// const startEditCategory = (category) => {
//   // Открыть модалку или инлайн-редактирование
// }
// const startEditSubcategory = (subcategory) => {
//   // Открыть модалку или инлайн-редактирование
// }

onMounted(async () => {
  await fetchUser()
  await fetchCategories()
  await fetchSubcategories()
})
</script>

<style scoped>
.categories-section {
  display: flex;
  gap: 2rem;
  margin-top: 2rem;
}
.category-list, .subcategory-list {
  flex: 1;
  background: #2a2a2a;
  padding: 1rem;
  border-radius: 8px;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  padding: 0.5rem;
  margin: 0.5rem 0;
  background: #333;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
button {
  background: none;
  border: none;
  color: #bb86fc;
  cursor: pointer;
  margin-left: 0.5rem;
}
.add-category, .add-subcategory {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}
input, select {
  background: #333;
  border: 1px solid #444;
  color: white;
  padding: 0.5rem;
  border-radius: 4px;
  flex-grow: 1;
}
</style>
