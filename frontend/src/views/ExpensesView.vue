<template>
    <section class="expenses container">
      <div class="table_view">
        <div class="search">
          <i class="fa-solid fa-magnifying-glass secondary"></i>
          <input 
            type="search" 
            v-model="searchQuery" 
            placeholder="Поиск по таблице"
          >
        </div>
        
        <div class="table_container">
          <table class="expenses_table">
            <thead>
              <tr>
                <th v-for="header in headers" :key="header">{{ header }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(expense, index) in filteredExpenses" :key="index">
                <td>{{ expense.date }}</td>
                <td>{{ expense.name }}</td>
                <td>{{ expense.price }}</td>
                <td>{{ expense.unit }}</td>
                <td>{{ expense.unit_quantity }}</td>
                <td>{{ expense.product_quantity }}</td>
                <td>{{ expense.category }}</td>
                <td>{{ expense.subcategory }}</td>
                <td class="modify">
                  <button class="mbtn" @click="editExpense(expense)">
                    <span class="fa-solid fa-pen"></span>
                  </button>
                  <button class="mbtn" @click="deleteExpense(expense)">
                    <span class="fa-solid fa-trash"></span>
                  </button>
                </td>
              </tr>
              
              <tr class="new_row">
                <td><input type="date" v-model="newExpense.date"></td>
                <td><input type="text" v-model="newExpense.name"></td>
                <td><input type="number" v-model="newExpense.price"></td>
                <td>
                  <select v-model="newExpense.unit">
                    <option value="л">л</option>
                    <option value="кг">кг</option>
                    <option value="г">г</option>
                    <option value="шт">шт</option>
                    <option value="мл">мл</option>
                  </select>
                </td>
                <td><input type="number" v-model="newExpense.unit_quantity"></td>
                <td><input type="number" v-model="newExpense.product_quantity"></td>
                <td>
                  <select v-model="newExpense.category">
                    <option v-for="cat in categories" :value="cat" :key="cat">{{ cat }}</option>
                  </select>
                </td>
                <td>
                  <select v-model="newExpense.subcategory">
                    <option value="Овощи">Овощи</option>
                    <option value="М">М</option>
                    <option value="A">A</option>
                  </select>
                </td>
                <td>
                  <button @click="addExpense">✓</button>
                  <button @click="cancelAdd">✕</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <button class="add_row_btn secondary" @click="showAddRow = true">
          Добавить запись
        </button>
      </div>
    </section>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue'
  
  export default {
    setup() {
      const headers = ref([
        'Дата', 'Название', 'Цена товара', 'Единица измерения',
        'Количество единицы измерения', 'Количество товара',
        'Категория', 'Подкатегории', 'Действия'
      ])
      
      const searchQuery = ref('')
      const showAddRow = ref(false)
      
      const categories = ref([
        'Сладкое', 'Базовые товары', 'Товары второй важности',
        'Бытовые продукты', 'Разовая покупка', 'Аренда квартиры',
        'Коммунальные услуги', 'Сигареты', 'Различные услуги',
        'Еда вне дома'
      ])
      
      const expenses = ref([
        // Пример данных, замените на реальные из API
        {
          id: 1,
          date: '2024-08-19',
          name: 'сливки',
          price: 155,
          unit: 'мл',
          unit_quantity: 400,
          product_quantity: 1,
          category: 'Товары первой важности',
          subcategory: 'Овощи'
        },
        // ... другие записи
      ])
      
      const newExpense = ref({
        date: new Date().toISOString().split('T')[0],
        name: '',
        price: 0,
        unit: 'г',
        unit_quantity: 0,
        product_quantity: 1,
        category: 'Базовые товары',
        subcategory: 'Овощи'
      })
      
      const filteredExpenses = computed(() => {
        return expenses.value.filter(expense => 
          expense.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          expense.category.toLowerCase().includes(searchQuery.value.toLowerCase())
        )
      })
      
      const addExpense = () => {
        expenses.value.push({ ...newExpense.value })
        // Здесь отправка на сервер
        resetNewExpense()
      }
      
      const cancelAdd = () => {
        resetNewExpense()
      }
      
      const resetNewExpense = () => {
        newExpense.value = {
          date: new Date().toISOString().split('T')[0],
          name: '',
          price: 0,
          unit: 'г',
          unit_quantity: 0,
          product_quantity: 1,
          category: 'Базовые товары',
          subcategory: 'Овощи'
        }
      }
      
      const editExpense = (expense) => {
        // Реализация редактирования
        return expense + ' edit'
      }
      
      const deleteExpense = (expense) => {
        // Реализация удаления
        return expense + ' delete'
      }
      
      onMounted(() => {
        // Загрузка данных с сервера
      })
      
      return {
        headers,
        searchQuery,
        showAddRow,
        categories,
        expenses,
        newExpense,
        filteredExpenses,
        addExpense,
        cancelAdd,
        editExpense,
        deleteExpense
      }
    }
  }
  </script>
  
  <style scoped>
  /* @import '@/assets/table.css'; */
  </style>