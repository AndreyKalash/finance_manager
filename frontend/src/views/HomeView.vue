<template>
    <main class="main">
      <section class="expenses_chart_items">
        <div class="expenses_chart container">
          <h2 class="title primary">Траты за {{ currentMonth }}</h2>
          <div class="chart_container">
            <i class="fa-solid fa-caret-left secondary nav_arrow" @click="prevMonth"></i>
            <div class="pie_chart">
              <canvas ref="sumChart"></canvas>
            </div>
            <i class="fa-solid fa-caret-right secondary nav_arrow" @click="nextMonth"></i>
          </div>
        </div>
  
        <div class="expenses_chart container">
          <h2 class="title primary">Траты за {{ currentMonth }}</h2>
          <div class="chart_container">
            <i class="fa-solid fa-caret-left secondary nav_arrow" @click="prevMonth"></i>
            <div class="pie_chart">
              <canvas ref="countChart"></canvas>
            </div>
            <i class="fa-solid fa-caret-right secondary nav_arrow" @click="nextMonth"></i>
          </div>
        </div>
      </section>
  
      <section class="expenses container">
        <div class="table_view">
          <router-link to="/expenses" class="secondary" title="Перейти на страницу трат">
            <h2 class="title primary">Таблица трат</h2>
          </router-link>
          <ExpensesTable :items="recentExpenses" :headers="headers" />
        </div>
      </section>
    </main>
  </template>
  
  <script>
  import { ref, onMounted, computed } from 'vue'
  import { Chart, registerables } from 'chart.js'
  import ExpensesTable from '@/components/ExpensesTable.vue'
  
  Chart.register(...registerables)
  
  export default {
    components: {
      ExpensesTable
    },
    setup() {
      const sumChart = ref(null)
      const countChart = ref(null)
      const currentDate = ref(new Date())
      
      const headers = ref([
        'Дата', 'Название', 'Цена товара', 'Единица измерения',
        'Количество единицы измерения', 'Количество товара',
        'Категория', 'Подкатегории', 'Действия'
      ])
  
      const recentExpenses = ref([
        // Пример данных, замените на реальные из API
        {
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
  
      const currentMonth = computed(() => {
        return currentDate.value.toLocaleString('default', { month: 'long', year: 'numeric' })
      })
  
      const initCharts = () => {
        // График сумм
        new Chart(sumChart.value.getContext('2d'), {
          type: 'pie',
          data: {
            labels: ['Категория 1', 'Категория 2', 'Категория 3'],
            datasets: [{
              data: [300, 500, 200],
              backgroundColor: ['#bb86fc', '#03dac6', '#cf6679']
            }]
          }
        })
  
        // График количеств
        new Chart(countChart.value.getContext('2d'), {
          type: 'pie',
          data: {
            labels: ['Категория 1', 'Категория 2', 'Категория 3'],
            datasets: [{
              data: [10, 20, 5],
              backgroundColor: ['#bb86fc', '#03dac6', '#cf6679']
            }]
          }
        })
      }
  
      const prevMonth = () => {
        currentDate.value.setMonth(currentDate.value.getMonth() - 1)
        // Здесь запрос к API за новыми данными
      }
  
      const nextMonth = () => {
        currentDate.value.setMonth(currentDate.value.getMonth() + 1)
        // Здесь запрос к API за новыми данными
      }
  
      onMounted(() => {
        initCharts()
        // Здесь запрос к API за данными
      })
  
      return {
        sumChart,
        countChart,
        currentMonth,
        recentExpenses,
        headers,
        prevMonth,
        nextMonth
      }
    }
  }
  </script>
  
  <style scoped>
  @import '@/assets/main.css';
  </style>