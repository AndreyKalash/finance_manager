<template>
    <section>
      <div class="settings container">
        <h2 class="title primary">Категории</h2>
        
        <div class="categories-section">
          <div class="category-list">
            <h3>Основные категории</h3>
            <ul>
              <li v-for="category in mainCategories" :key="category.id">
                {{ category.name }}
                <button @click="editCategory(category)">
                  <i class="fa-solid fa-pen"></i>
                </button>
                <button @click="deleteCategory(category.id)">
                  <i class="fa-solid fa-trash"></i>
                </button>
              </li>
            </ul>
            
            <div class="add-category">
              <input v-model="newCategoryName" placeholder="Новая категория">
              <button @click="addCategory">Добавить</button>
            </div>
          </div>
          
          <div class="subcategory-list">
            <h3>Подкатегории</h3>
            <ul>
              <li v-for="subcategory in subcategories" :key="subcategory.id">
                {{ subcategory.name }} ({{ subcategory.category }})
                <button @click="editSubcategory(subcategory)">
                  <i class="fa-solid fa-pen"></i>
                </button>
                <button @click="deleteSubcategory(subcategory.id)">
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
              <input v-model="newSubcategoryName" placeholder="Новая подкатегория">
              <button @click="addSubcategory">Добавить</button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  
  export default {
    setup() {
      const mainCategories = ref([
        { id: 1, name: 'Товары первой важности' },
        { id: 2, name: 'Сладкое' },
        { id: 3, name: 'Бытовые продукты' }
      ])
      
      const subcategories = ref([
        { id: 1, name: 'Овощи', category: 'Товары первой важности', category_id: 1 },
        { id: 2, name: 'М', category: 'Товары первой важности', category_id: 1 },
        { id: 3, name: 'A', category: 'Сладкое', category_id: 2 }
      ])
      
      const newCategoryName = ref('')
      const newSubcategoryName = ref('')
      const newSubcategoryCategory = ref(1)
      
      const addCategory = () => {
        if (newCategoryName.value.trim()) {
          const newId = Math.max(...mainCategories.value.map(c => c.id), 0) + 1
          mainCategories.value.push({
            id: newId,
            name: newCategoryName.value.trim()
          })
          newCategoryName.value = ''
        }
      }
      
      const addSubcategory = () => {
        if (newSubcategoryName.value.trim()) {
          const category = mainCategories.value.find(c => c.id === newSubcategoryCategory.value)
          const newId = Math.max(...subcategories.value.map(s => s.id), 0) + 1
          
          subcategories.value.push({
            id: newId,
            name: newSubcategoryName.value.trim(),
            category: category.name,
            category_id: category.id
          })
          
          newSubcategoryName.value = ''
        }
      }
      
      const editCategory = (category) => {
        // Реализация редактирования
        return category + ' edit'
      }
      
      const deleteCategory = (id) => {
        mainCategories.value = mainCategories.value.filter(c => c.id !== id)
        subcategories.value = subcategories.value.filter(s => s.category_id !== id)
      }
      
      const editSubcategory = (subcategory) => {
        // Реализация редактирования
        return subcategory + ' edit'
      }
      
      const deleteSubcategory = (id) => {
        subcategories.value = subcategories.value.filter(s => s.id !== id)
      }
      
      onMounted(() => {
        // Загрузка данных с сервера
      })
      
      return {
        mainCategories,
        subcategories,
        newCategoryName,
        newSubcategoryName,
        newSubcategoryCategory,
        addCategory,
        addSubcategory,
        editCategory,
        deleteCategory,
        editSubcategory,
        deleteSubcategory
      }
    }
  }
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