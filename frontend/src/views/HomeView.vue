<template>
  <main class="main">
    <section class="expenses_chart_items">
      <div class="expenses_chart container">
        <h2 class="title primary">Траты за {{ currentMonth }}</h2>
        <div class="chart_container">
          <i class="fa-solid fa-caret-left secondary nav_arrow" @click="prevMonth"></i>
          <PieChart :chartData="sumChartData" />
          <i class="fa-solid fa-caret-right secondary nav_arrow" @click="nextMonth"></i>
        </div>
      </div>

      <div class="expenses_chart container">
        <h2 class="title primary">Траты за {{ currentMonth }}</h2>
        <div class="chart_container">
          <i class="fa-solid fa-caret-left secondary nav_arrow" @click="prevMonth"></i>
          <PieChart :chartData="countChartData" />
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

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from '@/api' // используйте ваш настроенный экземпляр axios
import PieChart from '@/components/layout/PieChart.vue'
import ExpensesTable from '@/components/ExpensesTable.vue'

const currentDate = ref(new Date())

const headers = ref([
  'Дата', 'Название', 'Цена товара', 'Единица измерения',
  'Количество единицы измерения', 'Количество товара',
  'Категория', 'Подкатегории', 'Действия'
])

const recentExpenses = ref([])
const sumChartData = ref({ labels: [], datasets: [{ data: [], backgroundColor: [] }] })
const countChartData = ref({ labels: [], datasets: [{ data: [], backgroundColor: [] }] })

const currentMonth = computed(() => {
  return currentDate.value.toLocaleString('default', { month: 'long', year: 'numeric' })
})

const fetchData = async () => {
  try {
    const month = currentDate.value.getMonth() + 1
    const year = currentDate.value.getFullYear()
    // Замените на ваши реальные эндпоинты
    const expensesRes = await axios.get(`/api/expenses?month=${month}&year=${year}`)
    const sumChartRes = await axios.get(`/api/expenses/sum-chart?month=${month}&year=${year}`)
    const countChartRes = await axios.get(`/api/expenses/count-chart?month=${month}&year=${year}`)

    recentExpenses.value = expensesRes.data

    sumChartData.value = {
      labels: sumChartRes.data.labels,
      datasets: [{
        data: sumChartRes.data.data,
        backgroundColor: sumChartRes.data.backgroundColor
      }]
    }

    countChartData.value = {
      labels: countChartRes.data.labels,
      datasets: [{
        data: countChartRes.data.data,
        backgroundColor: countChartRes.data.backgroundColor
      }]
    }
  } catch (error) {
    console.error('Ошибка загрузки данных:', error)
  }
}

onMounted(fetchData)

const prevMonth = () => {
  currentDate.value.setMonth(currentDate.value.getMonth() - 1)
  fetchData()
}

const nextMonth = () => {
  currentDate.value.setMonth(currentDate.value.getMonth() + 1)
  fetchData()
}

</script>

<style scoped>
@import '@/assets/main.css';
</style>
