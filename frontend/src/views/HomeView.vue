<template>
  <main class="main">
    <section class="records_chart_items">
      <div class="records_chart container">
        <div class="chart_container">
          <button class="nav_button left" @click="prevMonth" aria-label="Предыдущий месяц">
            <font-awesome-icon :icon="['fas', 'chevron-left']" />
          </button>
          <div class="center_content">
            <h2 class="title primary">Траты за {{ currentMonth }}</h2>
            <PieChart :chartData="sumChartData" />
          </div>
        </div>
      </div>

      <div class="records_chart container">
        <div class="chart_container">
          <div class="center_content">
            <h2 class="title primary">Количество трат за {{ currentMonth }}</h2>
            <PieChart :chartData="countChartData" />
          </div>
          <button
            class="nav_button right"
            :disabled="isCurrentMonth"
            @click="nextMonth"
            aria-label="Следующий месяц"
          >
            <font-awesome-icon :icon="['fas', 'chevron-right']" />
          </button>
        </div>
      </div>
    </section>

    <section class="records container">
      <div class="table_view">
        <router-link to="/records" class="secondary" title="Перейти на страницу трат">
          <h2 class="title primary">Таблица трат</h2>
        </router-link>
        <RecordsTable :items="recentRecords" :headers="headers" :fetch-charts="true" />
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import PieChart from '@/components/layout/PieChart.vue'
import RecordsTable from '@/components/RecordsTable.vue'
import { useRecordsStore } from '@/stores/records'
import { useStatsStore } from '@/stores/stats'
import { useCategoriesStore } from '@/stores/categories'
import { useAuthStore } from '@/stores/auth'
import { useTagsStore } from '@/stores/tags'
import { useUnitsStore } from '@/stores/units'

const currentDate = ref(new Date())
const recordsStore = useRecordsStore()
const statsStore = useStatsStore()
const authStore = useAuthStore()
const categoriesStore = useCategoriesStore()
const tagsStore = useTagsStore()
const unitsStore = useUnitsStore()

const headers = [
  'Дата', 'Название', 'Цена товара', 'Единица измерения',
  'Количество единицы измерения', 'Количество товара',
  'Категория', 'Теги'
]

const currentMonth = computed(() => {
  return currentDate.value.toLocaleString('default', { month: 'long', year: 'numeric' })
})

const month = computed(() => currentDate.value.getMonth() + 1)
const year = computed(() => currentDate.value.getFullYear())

const recentRecords = computed(() => recordsStore.records.slice(0, 10))

const sumChartData = computed(() => ({
  labels: statsStore.categoriesMonthSum.map(item => item.category),
  datasets: [{
    data: statsStore.categoriesMonthSum.map(item => item.sum),
    backgroundColor: statsStore.categoriesMonthSum.map(item => item.color)
  }]
}))

const countChartData = computed(() => ({
  labels: statsStore.categoriesMonthCount.map(item => item.category),
  datasets: [{
    data: statsStore.categoriesMonthCount.map(item => item.count),
    backgroundColor: statsStore.categoriesMonthCount.map(item => item.color)
  }]
}))

const isCurrentMonth = computed(() => {
  const now = new Date()
  return (
    currentDate.value.getMonth() === now.getMonth() &&
    currentDate.value.getFullYear() === now.getFullYear()
  )
})

const prevMonth = async () => {
  const d = new Date(currentDate.value)
  d.setMonth(d.getMonth() - 1)
  currentDate.value = d
  await statsStore.fetchStats(month.value, year.value)
}

const nextMonth = async () => {
  const d = new Date(currentDate.value)
  d.setMonth(d.getMonth() + 1)
  currentDate.value = d
  await statsStore.fetchStats(month.value, year.value)
}

onMounted(async () => {
  await authStore.fetchUser()
  await categoriesStore.fetchCategories()
  await tagsStore.fetchTags()
  await unitsStore.fetchUnits()
  await recordsStore.fetchRecords()
  await statsStore.fetchStats(month.value, year.value)
})

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
  padding: 20px;
  border-radius: 8px;
}

.chart_container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 10px 0;
  gap: 0;
  min-height: 370px;
}

.center_content {
  flex: 1 1 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.nav_button {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #2a2a2a;
  border: 1px solid #444;
  color: #bb86fc;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav_button:hover {
  background-color: #3a3a3a;
  color: #03dac6;
  transform: scale(1.1);
}

.nav_button:active {
  transform: scale(0.95);
}

.nav_button i {
  font-size: 18px;
}

.nav_button.left {
  margin-left: 10px;
}

.nav_button.right {
  margin-right: 10px;
}

.nav_button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}
</style>
