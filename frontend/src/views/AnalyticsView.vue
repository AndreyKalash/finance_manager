<template>

    <section class="records_chart_items">
        <div class="records_chart container">
            <div class="chart_container">
                <div class="center_content">
                    <AppChart :key="currentType.name" :chart-type="'line'" :chart-data="trendData" :chart-options="chartOptions" />

                </div>
            </div>
        </div>
    </section>
    <section class="container">
        <div class="filter-section">
            <div class="date-range">
                <input v-model="startDate" type="date" class="date-input" @change="updateFilters" />
                <span class="date-separator">—</span>
                <input v-model="endDate" type="date" class="date-input" @change="updateFilters" />
            </div>

            <div class="filter-dropdown">
                <label>{{ 'Тип операции' + (currentType ? `: ${currentType.text}` : '') }}</label>
                <AppDropdown :items="operationTypes" v-model="currentType" placeholder="Тип операции" name-key="text"
                    value-key="value" @select="handleSelectType" :search="true" />
            </div>

            <div class="filter-dropdown">
                <label>Категории</label>
                <AppDropdown :show-color="true" :items="categories" placeholder="Выберите категории" name-key="name"
                    :search="true" v-model="selectedCategories" :multiple="true" color-key="color"
                    @update:modelValue="updateFilters" />
            </div>

            <div class="filter-dropdown">
                <label>Теги</label>
                <AppDropdown :show-color="true" :items="filteredTags" placeholder="Выберите теги" name-key="name"
                    :search="true" v-model="selectedTags" :multiple="true" color-key="color"
                    @update:modelValue="updateFilters" />
            </div>

            <div v-if="currentType.name == RTYPES.expense" class="filter-dropdown">
                <label>Единицы измерения</label>
                <AppDropdown :items="unitsWithAll" placeholder="Все единицы" name-key="name" :search="true"
                    v-model="selectedUnit" :multiple="true" @update:modelValue="updateFilters" />
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { RTYPES } from "@/utils/recordTypes";
import { useStatsStore } from "@/stores/stats";
import { useCategoriesStore } from "@/stores/categories";
import { useTagsStore } from "@/stores/tags";
import { useUnitsStore } from "@/stores/units";
import AppDropdown from "@/components/layout/AppDropdown.vue";
import AppChart from "@/components/layout/AppChart.vue";

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

const handleSelectType = async (value) => {
    currentType.value = value
    await updateFilters();
}

function getDefaultStartDate() {
    const date = new Date();
    date.setDate(date.getDate() - 30);
    return date.toISOString().split('T')[0];
}

function getDefaultEndDate() {
    return new Date().toISOString().split('T')[0];
}

async function updateFilters() {
    const filters = {
        start_date: startDate.value,
        end_date: endDate.value,
        categories: selectedCategories.value,
        tags: selectedTags.value,
        units: selectedUnit.value
    };
    await statsStore.fetchCustomCharts(currentType.value.name, filters);
}

const trendData = computed(() => {
  const labels = statsStore.trend.map(item => item.date);
  const data = statsStore.trend.map(item => item.amount_sum);
  
  return {
    labels,
    datasets: [{
      label: 'Сумма',
      data,
      borderColor: currentType.value.name === 'expense' ? '#9B59B6' : '#2ECC71',
      borderWidth: 2,
      tension: 0.4, 
      pointRadius: 3,
      fill: false
    }]
  };
});

const chartOptions = computed(() => ({
  responsive: true,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    x: {
      grid: { display: false }
    },
    y: {
      beginAtZero: true
    }
  }
}));

onMounted(async () => {
    await Promise.all([
        categoriesStore.fetchCategories(),
        tagsStore.fetchTags(),
        unitsStore.fetchUnits()
    ]);

    updateFilters();
});

watch(currentType, async () => {
    selectedCategories.value = [];
    selectedTags.value = [];
    await updateFilters();
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
}
</style>
