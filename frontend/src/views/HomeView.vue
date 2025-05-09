<template>
  <main class="main">
    <section class="records_chart_items">
      <div class="records_chart container">
        <h2 class="title primary">Траты за {{ currentMonth }}</h2>
        <div class="chart_container">
          <i class="fa-solid fa-caret-left secondary nav_arrow" @click="prevMonth"></i>
          <PieChart :chartData="sumChartData" />
          <i class="fa-solid fa-caret-right secondary nav_arrow" @click="nextMonth"></i>
        </div>
      </div>

      <div class="records_chart container">
        <h2 class="title primary">Траты за {{ currentMonth }}</h2>
        <div class="chart_container">
          <i class="fa-solid fa-caret-left secondary nav_arrow" @click="prevMonth"></i>
          <PieChart :chartData="countChartData" />
          <i class="fa-solid fa-caret-right secondary nav_arrow" @click="nextMonth"></i>
        </div>
      </div>
    </section>

    <section class="records container">
      <div class="table_view">
        <router-link to="/records" class="secondary" title="Перейти на страницу трат">
          <h2 class="title primary">Таблица трат</h2>
        </router-link>
        <RecordsTable :items="recentRecords" :headers="headers" />
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from '@/api' // используйте ваш настроенный экземпляр axios
import PieChart from '@/components/layout/PieChart.vue'
import RecordsTable from '@/components/RecordsTable.vue'

const currentDate = ref(new Date())

const headers = ref([
  'Дата', 'Название', 'Цена товара', 'Единица измерения',
  'Количество единицы измерения', 'Количество товара',
  'Категория', 'Подкатегории', 'Действия'
])

const recentRecords = ref([])
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
    const recordsRes = await axios.get(`/api/records?month=${month}&year=${year}`)
    const sumChartRes = await axios.get(`/api/records/sum-chart?month=${month}&year=${year}`)
    const countChartRes = await axios.get(`/api/records/count-chart?month=${month}&year=${year}`)

    recentRecords.value = recordsRes.data

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
.records_chart_items {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 20px;
}
.records_chart {
    display: flex;
    flex: 1;
    flex-direction: column;
    align-items: center;
    background-color: #1e1e1e;
}
.chart_container {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.nav_arrow {
    font-size: 30px;
}
.nav_arrow:hover{
    cursor: pointer;
}

</style>
