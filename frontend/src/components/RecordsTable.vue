<!-- RecordsTable.vue -->
<template>
  <div class="table_view">
    <!-- Блок переключения между типами записей -->
    <div class="tabs">
      <button v-for="type in types" :key="type.value" :class="['tab-btn', { active: currentType === type.value }]"
        @click="changeType(type.value)">
        {{ type.label }}
      </button>
    </div>
    <!-- Поисковая строка с иконкой -->
    <div class="search" v-if="showSearch">
      <i class="fa-solid fa-magnifying-glass secondary"></i>
      <input type="search" v-model="searchQuery" placeholder="Поиск по таблице" id="records_search" />
    </div>
    <!-- Контейнер таблицы-->
    <div class="table_container" @mouseenter="onTableMouseEnter" @mouseleave="onTableMouseLeave">
      <table class="records_table">
        <thead>
          <tr>
            <th v-for="header in headers" :key="header">{{ header }}</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in filteredItems" :key="index">
            <td>{{ item.record_date }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.amount }}</td>
            <template v-if="currentType === RTYPES.expense">
              <td>{{ item.unit.name }}</td>
              <td>{{ item.unit_quantity }}</td>
              <td>{{ item.product_quantity }}</td>
            </template>
            <td>
              <span v-if="item.category" class="category-badge">
                <span class="color-badge" :style="{ backgroundColor: item.category.color }"></span>
                {{ item.category.name }}
              </span>
            </td>
            <td>
              <div class="tags-cell">
                <template v-if="item.tags.length <= 3">
                  <span v-for="tag in item.tags" :key="tag.id" class="tag-badge">
                    <span class="color-badge" :style="{ backgroundColor: tag.color }"></span>
                    {{ tag.name }}
                  </span>
                </template>
                <template v-else>
                  <span v-for="(tag, idx) in item.tags.slice(0, 2)" :key="tag.id" class="tag-badge">
                    <span class="color-badge" :style="{ backgroundColor: tag.color }"></span>
                    {{ tag.name }}
                    <span v-if="idx < 1" class="tag-separator">,</span>
                  </span>
                  <span class="tag-badge more-badge" @mouseenter="showTooltip = index" @mouseleave="showTooltip = null">
                    +{{ item.tags.length - 2 }}
                    <span v-if="showTooltip === index" class="tag-tooltip">
                      <span v-for="tag in item.tags.slice(2)" :key="tag.id" class="tag-badge">
                        <span class="color-badge" :style="{ backgroundColor: tag.color }"></span>
                        {{ tag.name }}
                      </span>
                    </span>
                  </span>
                </template>
              </div>
            </td>
            <td class="modify">
              <button class="mbtn" @click="editRecord(item)">✎</button>
              <button class="mbtn" @click="deleteRecord(currentType, item)">🗑</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- Модальное окно редактирования/создания -->
    <RecordFormModal v-model="formModalVisible" :record-to-edit="editingRecord" :categories="categories" :tags="tags"
      :units="units" :type="currentType" @create="createRecord" @update="updateRecord" />
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import RecordFormModal from "./layout/RecordFormModal.vue";
import { useCategoriesStore } from "@/stores/categories";
import { useTagsStore } from "@/stores/tags";
import { useUnitsStore } from "@/stores/units";
import { useRecordsStore } from "@/stores/records";
import { useStatsStore } from "@/stores/stats";
import { RTYPES } from "@/utils/recordTypes.js";

const props = defineProps({
  items: { type: Array, default: () => [] },
  showSearch: { type: Boolean, default: false },
  fetchCharts: { type: Boolean, default: false },
  modelValue: { type: String, default: RTYPES.expense },
  headers: { type: Array, required: false }
});

const headers = computed(() => {
  const typedHeaders = currentType.value === RTYPES.expense
    ? ["Цена товара", "Единица измерения", "Количество единицы измерения", "Количество товара"]
    : ["Сумма"]

  return [
    "Дата",
    "Название",
    ...typedHeaders,
    "Категория",
    "Теги",
  ]
})

const emit = defineEmits(["update:modelValue"]);

const types = [
  { value: RTYPES.expense, label: "Траты" },
  { value: RTYPES.income, label: "Доходы" },
];

const currentType = ref(props.modelValue);

const categoryStore = useCategoriesStore();
const tagStore = useTagsStore();
const unitStore = useUnitsStore();
const recordsStore = useRecordsStore();
const statsStore = useStatsStore();

const searchQuery = ref("");
const tableHover = ref(false);
const formModalVisible = ref(false);
const editingRecord = ref(null);
const showTooltip = ref(null);

const categories = computed(() => categoryStore.categories[currentType.value] || []);
const tags = computed(() => tagStore.tags[currentType.value] || []);
const units = computed(() => unitStore.units || []);

watch(
  () => props.modelValue,
  (val) => {
    if (val && val !== currentType.value) currentType.value = val;
  }
);

function changeType(type) {
  currentType.value = type;
  emit("update:modelValue", currentType.value);
}

const filteredItems = computed(() => {
  const items = props.items || [];
  if (!searchQuery.value) return items;
  return items.filter((item) =>
    (item.name ?? "").toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

function onTableMouseEnter() {
  tableHover.value = true;
}
function onTableMouseLeave() {
  tableHover.value = false;
}

function showFormModal(record = null) {
  editingRecord.value = record;
  formModalVisible.value = true;
}

function editRecord(record) {
  showFormModal(record);
}

async function createRecord(type, record) {
  await recordsStore.createRecord(type, record);
  formModalVisible.value = false;
}

async function updateRecord(type, record) {
  await recordsStore.updateRecord(type, record);
  formModalVisible.value = false;
  editingRecord.value = null;
  if (props.fetchCharts) {
    await fetchCharts(type, record);
  }
}

async function deleteRecord(type, record) {
  if (confirm("Вы уверены, что хотите удалить эту запись?" + type + record)) {
    await recordsStore.deleteRecord(type, record.id);
    if (props.fetchCharts) {
      await fetchCharts(type, record);
    }
  }
}

async function fetchCharts(type, record) {
  const record_date = new Date(record.record_date);
  if (
    record_date.getMonth() + 1 == statsStore.currentChartMonth &&
    record_date.getFullYear() == statsStore.currentChartYear
  ) {
    await statsStore.fetchStats(
      type,
      record_date.getMonth() + 1,
      record_date.getFullYear()
    );
  }
}

defineExpose({ showFormModal });
</script>

<style scoped>
.tabs {
  display: flex;
  gap: 10px;
}

.tab-btn {
  padding: 8px 22px;
  border: none;
  border-radius: 7px 7px 0 0;
  background: #29293b;
  color: #bb86fc;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  transition: background 0.2s;
}

.tab-btn.active {
  background: #03dac6;
  color: #232323;
  font-weight: bold;
  box-shadow: 0 -2px 8px #03dac655;
}

.tab-btn:not(.active):hover {
  background: #333;
}

.table_view {
  display: flex;
  flex-direction: column;
}

.table_container {
  overflow-x: auto;
  overflow-y: auto;
  max-height: 600px;
  border: 1px solid #bb86fc;
  position: relative;
  scrollbar-color: #03dac6;
}

.search {
  display: flex;
  align-items: center;
}

#records_search {
  padding: 5px;
  width: 100%;
  background-color: #2b2b2b;
  border: 1px solid #bb86fc;
  border-radius: 5px;
  color: #d9cfcf;
}

#records_search:hover {
  background-color: #333;
}

#records_search:focus {
  outline: none;
  box-shadow: none;
  border-color: #03dac6;
}

.fa-magnifying-glass {
  font-size: 20px;
  margin-right: 15px;
}

.records_table {
  width: 100%;
  border-collapse: collapse;
}

.records_table tr {
  text-align: center;
}

.records_table th {
  background-color: #333;
  color: #f5f5f5;
  font-weight: bold;
  padding: 10px;
  border: 1px solid #444;
}

.records_table td {
  color: #e0e0e0;
  padding: 10px;
  border: 1px solid #444;
  vertical-align: middle;
}

.records_table tr:nth-child(odd) {
  background-color: #2a2a2a;
}

.records_table tr:nth-child(even) {
  background-color: #1e1e1e;
}

.records_table tr:hover {
  background-color: #333;
}

.mbtn {
  background: none;
  border: none;
  cursor: pointer;
  color: #bb86fc;
  font-size: 18px;
  padding: 5px;
}

.category-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #26263a;
  border-radius: 6px;
  padding: 2px 8px;
  font-size: 0.98em;
  font-weight: 500;
}

.color-badge {
  width: 14px;
  height: 14px;
  border-radius: 3px;
  display: inline-block;
  margin-right: 4px;
  border: 1.5px solid #444;
  vertical-align: middle;
}

.tags-cell {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
  min-width: 80px;
}

.tag-badge {
  display: inline-flex;
  align-items: center;
  background: #23232b;
  border-radius: 7px;
  padding: 2px 7px;
  font-size: 0.93em;
  margin-right: 2px;
  border: 1px solid #444;
  color: #e0e0e0;
  transition: background 0.18s;
  position: relative;
}

.tag-separator {
  margin: 0 2px;
  color: #888;
}

.more-badge {
  background: #3a3a4a;
  color: #bb86fc;
  cursor: pointer;
  border: 1px dashed #bb86fc;
  font-weight: bold;
  padding: 2px 8px;
  position: relative;
}

.tag-tooltip {
  display: block;
  position: absolute;
  top: 120%;
  left: 0;
  background: #23232b;
  color: #e0e0e0;
  border: 1px solid #bb86fc;
  border-radius: 7px;
  padding: 8px 12px;
  min-width: 120px;
  z-index: 100;
  box-shadow: 0 2px 12px #0007;
  white-space: nowrap;
}

.tag-tooltip .tag-badge {
  margin: 2px 0;
  background: #29293b;
}
</style>
