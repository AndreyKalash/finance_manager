<!-- AnalyticsView.vue -->
<template>
  <!-- Секция для отображения графиков -->
  <section class="records_chart_items">
    <div class="records_chart container">
      <div class="chart_container">
        <div class="center_content">
          <div v-if="isLoading" class="loading-spinner">
            Загрузка...
          </div>
          <!-- Компонент графика с уникальным ключом для принудительного ререндера -->
          <AppChart v-else-if="!isLoading && trendData.datasets.length > 0"
            :chart-key="`chart-${currentType.name}-${dataKey}`" :chart-type="'line'" :chart-data="trendData"
            :chart-options="chartOptions" />
        </div>
      </div>
    </div>
  </section>
  <!-- Секция фильтров -->
  <section class="container">
    <div class="filter-section">
      <div class="date-range">
        <input v-model="startDate" type="date" class="date-input" />
        <span class="date-separator">—</span>
        <input v-model="endDate" type="date" class="date-input" />
      </div>

      <div class="filter-dropdown">
        <label>{{ 'Тип операции' + (currentType ? `: ${currentType.text}` : '') }}</label>
        <AppDropdown :items="operationTypes" v-model="currentType.name" placeholder="Тип операции" name-key="text"
          value-key="value" @select="handleSelectType" :search="true" :disabled="isLoading" />
      </div>

      <div class="filter-dropdown">
        <label>Категории</label>
        <AppDropdown :show-color="true" :items="categories" placeholder="Выберите категории" name-key="name"
          :search="true" v-model="selectedCategories" :multiple="true" color-key="color" :disabled="isLoading" />
      </div>

      <div class="filter-dropdown">
        <label>Теги</label>
        <AppDropdown :show-color="true" :items="filteredTags" placeholder="Выберите теги" name-key="name" :search="true"
          v-model="selectedTags" :multiple="true" color-key="color" :disabled="isLoading" />
      </div>

      <div v-if="currentType.name == RTYPES.expense" class="filter-dropdown">
        <label>Единицы измерения</label>
        <AppDropdown :items="unitsWithAll" placeholder="Все единицы" name-key="name" :search="true"
          v-model="selectedUnit" :multiple="true" :disabled="isLoading" />
      </div>

    </div>
    <!-- Кнопка применения фильтров -->
    <button class="apply-button" @click="applyFilters" :disabled="isLoading">
      Применить
    </button>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from "vue";
import { RTYPES } from "@/utils/recordTypes";
import { useStatsStore } from "@/stores/stats";
import { useCategoriesStore } from "@/stores/categories";
import { useTagsStore } from "@/stores/tags";
import { useUnitsStore } from "@/stores/units";
import AppDropdown from "@/components/layout/AppDropdown.vue";
import AppChart from "@/components/layout/AppChart.vue";
import { isEqual } from 'lodash-es'; //

const statsStore = useStatsStore();
const categoriesStore = useCategoriesStore();
const tagsStore = useTagsStore();
const unitsStore = useUnitsStore();

const startDate = ref(getDefaultStartDate());
const endDate = ref(getDefaultEndDate());
const currentType = ref({ text: 'Траты', name: RTYPES.expense });
const selectedCategories = ref([]);
const selectedTags = ref([]);
const selectedUnit = ref([]);

const operationTypes = ref([
  { text: 'Траты', name: RTYPES.expense },
  { text: 'Доходы', name: RTYPES.income },
]);

const unitsWithAll = computed(() => [
  { id: '', name: 'Все единицы' },
  ...unitsStore.units,
]);

const categories = computed(() => categoriesStore.categories[currentType.value.name]);
const filteredTags = computed(() => tagsStore.tags[currentType.value.name]);

const isLoading = ref(false);
const dataKey = ref(0);
const lastAppliedFilters = ref(null);

function getDefaultStartDate() {
  const date = new Date();
  date.setDate(date.getDate() - 30);
  return date.toISOString().split('T')[0];
}

function getDefaultEndDate() {
  return new Date().toISOString().split('T')[0];
}
// Обработчик смены типа операции
const handleSelectType = async (value) => {
  if (isLoading.value || currentType.value.name == value.name) return;
  lastAppliedFilters.value = null;
  isLoading.value = true;
  try {
    currentType.value = value;
    await nextTick();
    await applyFilters()
    dataKey.value++;
  } catch (error) {
    console.error('Ошибка при смене типа:', error);
  } finally {
    setTimeout(() => {
      isLoading.value = false;
    }, 500);
  }
};
// Применение фильтров с проверкой изменений
const applyFilters = async (needCheck = true) => {
  const currentFilters = {
    start_date: startDate.value,
    end_date: endDate.value,
    categories: selectedCategories.value,
    tags: selectedTags.value,
    units: selectedUnit.value
  };
  if (needCheck && isEqual(currentFilters, lastAppliedFilters.value)) {
    isLoading.value = false;
    return;
  }
  try {
    isLoading.value = true;
    await statsStore.fetchCustomCharts(currentType.value.name, currentFilters);
    lastAppliedFilters.value = JSON.parse(JSON.stringify(currentFilters));
    dataKey.value++;
  } catch (error) {
    console.error('Ошибка при применении фильтров:', error);
  } finally {
    isLoading.value = false;
  }
};
// Конфигурация отображения для разных типов операций
const typeConfig = computed(() => {
  const configs = {
    [RTYPES.expense]: {
      color: '#9B59B6',
      label: 'Расходы',
      unitSymbol: '₽'
    },
    [RTYPES.income]: {
      color: '#2ECC71',
      label: 'Доходы',
      unitSymbol: '₽'
    }
  };

  return configs[currentType.value.name];
});
// Формирование данных для графика
const trendData = computed(() => {
  const trend = statsStore.trend
  const labels = trend.map(item => item.date);
  const data = trend.map(item => item.amount_sum);
  const config = typeConfig.value;

  return {
    labels,
    datasets: [{
      label: config.label,
      data,
      borderColor: config.color,
      backgroundColor: config.color + '20',
      borderWidth: 2,
      tension: 0.4,
      pointRadius: 3,
      pointBackgroundColor: config.color,
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      fill: false
    }]
  };
});
// Настройки отображения графика
const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top',
      labels: {
        color: '#fff',
        font: {
          size: 14
        }
      }
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleColor: '#fff',
      bodyColor: '#fff',
      borderColor: typeConfig.value.color,
      borderWidth: 1,
      callbacks: {
        label: (ctx) => `${ctx.parsed.y.toLocaleString()} ${typeConfig.value.unitSymbol}`
      }
    }
  },
  scales: {
    x: {
      grid: {
        display: false
      },
      ticks: {
        color: '#9CA3AF'
      }
    },
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(156, 163, 175, 0.1)'
      },
      ticks: {
        color: '#9CA3AF',
        callback: function (value) {
          return value.toLocaleString() + ' ' + typeConfig.value.unitSymbol;
        }
      }
    }
  },
  elements: {
    point: {
      hoverRadius: 6
    }
  }
}));

onMounted(async () => {
  try {
    await Promise.all([
      categoriesStore.fetchCategories(),
      tagsStore.fetchTags(),
      unitsStore.fetchUnits()
    ]);

    await nextTick();
    await new Promise(resolve => requestAnimationFrame(resolve));
    await applyFilters(false);
  } catch (error) {
    console.error('Ошибка при инициализации:', error);
  }
});
</script>

<style scoped>
.filter-section {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 2rem;
  padding: 1.5rem 2rem;
  background: var(--color-background-soft, #2a2a2a);
  border-radius: 12px;
  box-shadow:
    0 2px 16px 0 rgba(0, 0, 0, 0.07),
    0 1px 3px rgba(0, 0, 0, 0.1);
  position: relative;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  position: relative;
}

.records_chart_items {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 20px;
  margin: 0px 20px;
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

.date-input {
  min-width: 10px;
  padding: 0.7rem 1.2rem;
  border: 1.5px solid #3a3f47;
  border-radius: 8px;
  background: #23272b;
  color: #fff;
  font-size: 0.95em;
  transition:
    border-color 0.25s ease,
    box-shadow 0.25s ease;
}

.date-input:focus {
  border-color: #5e81f4;
  box-shadow: 0 0 0 3px rgba(94, 129, 244, 0.15);
  outline: none;
}

.date-separator {
  color: #6b7280;
  font-size: 1.1em;
  margin: 0 0.2rem;
}

.filter-dropdown {
  display: flex;
  flex-direction: column;
  min-width: 220px;
  gap: 0.6rem;
  position: relative;
}

.filter-dropdown label {
  font-size: 0.95em;
  color: #b7bbc4;
  font-weight: 500;
  margin-bottom: 0.3em;
  padding-left: 0.3rem;
}

.AppDropdown,
.app-dropdown,
.dropdown-wrapper {
  width: 100%;
  transition: transform 0.2s ease;
}

.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #9CA3AF;
  font-size: 1.1em;
}

.center_content {
  transition: opacity 0.3s ease;
}

.apply-button {
  padding: 0.8rem 1.5rem;
  color: black;
  border: none;
  background-color: #03dac6;
  margin-top: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition:
    background-color 0.25s ease,
    transform 0.15s ease;
  font-weight: 500;
  align-self: center;
}

.apply-button:hover {
  background: #0ea192;
}

.apply-button:active {
  transform: scale(0.98);
}

.apply-button:disabled {
  background: #4b5563;
  cursor: not-allowed;
  opacity: 0.7;
}


@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 1100px) {
  .filter-section {
    gap: 1.5rem;
    padding: 1.2rem;
  }

  .filter-dropdown {
    min-width: 180px;
  }

  .date-input {
    min-width: 120px;
    padding: 0.6rem 1rem;
  }
}

@media (max-width: 700px) {
  .filter-section {
    flex-direction: column;
    align-items: stretch;
    gap: 1.2rem;
    padding: 1.2rem;
  }

  .date-range {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
    margin-right: 0;
  }

  .date-input {
    min-width: auto;
  }

  .filter-dropdown {
    min-width: auto;
  }

  .apply-button {
    width: 100%;
    margin-top: 1rem;
  }
}
</style>
