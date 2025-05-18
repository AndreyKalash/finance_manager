<template>
  <div class="table_view">
    <div class="search" v-if="showSearch">
      <i class="fa-solid fa-magnifying-glass secondary"></i>
      <input
        type="search"
        v-model="searchQuery"
        placeholder="Поиск по таблице"
        id="records_search"
      />
    </div>

    <div
      class="table_container"
      @mouseenter="onTableMouseEnter"
      @mouseleave="onTableMouseLeave"
    >
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
            <td>{{ item.price }}</td>
            <td>{{ item.unit.name }}</td>
            <td>{{ item.unit_quantity }}</td>
            <td>{{ item.product_quantity }}</td>
            <td>
              <span v-if="item.category" class="category-badge">
                <span
                  class="color-badge"
                  :style="{ backgroundColor: item.category.color }"
                ></span>
                {{ item.category.name }}
              </span>
            </td>
            <td>
              <div class="tags-cell">
                <template v-if="item.tags.length <= 3">
                  <span
                    v-for="tag in item.tags"
                    :key="tag.id"
                    class="tag-badge"
                  >
                    <span
                      class="color-badge"
                      :style="{ backgroundColor: tag.color }"
                    ></span>
                    {{ tag.name }}
                  </span>
                </template>
                <template v-else>
                  <span
                    v-for="(tag, idx) in item.tags.slice(0, 2)"
                    :key="tag.id"
                    class="tag-badge"
                  >
                    <span
                      class="color-badge"
                      :style="{ backgroundColor: tag.color }"
                    ></span>
                    {{ tag.name }}
                    <span v-if="idx < 1" class="tag-separator">,</span>
                  </span>
                  <span
                    class="tag-badge more-badge"
                    @mouseenter="showTooltip = index"
                    @mouseleave="showTooltip = null"
                  >
                    +{{ item.tags.length - 2 }}
                    <span v-if="showTooltip === index" class="tag-tooltip">
                      <span
                        v-for="tag in item.tags.slice(2)"
                        :key="tag.id"
                        class="tag-badge"
                      >
                        <span
                          class="color-badge"
                          :style="{ backgroundColor: tag.color }"
                        ></span>
                        {{ tag.name }}
                      </span>
                    </span>
                  </span>
                </template>
              </div>
            </td>
            <td class="modify">
              <button class="mbtn" @click="editRecord(item)">✎</button>
              <button class="mbtn" @click="deleteRecord(item)">🗑</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <RecordFormModal
      v-model="formModalVisible"
      :record-to-edit="editingRecord"
      :categories="categories"
      :tags="tags"
      :units="units"
      @create="createRecord"
      @update="updateRecord"
    />
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import RecordFormModal from "./layout/RecordFormModal.vue";
import { useCategoriesStore } from "@/stores/categories";
import { useTagsStore } from "@/stores/tags";
import { useUnitsStore } from "@/stores/units";
import { useRecordsStore } from "@/stores/records";
import { useStatsStore } from "@/stores/stats";

const props = defineProps({
  items: { type: Array, default: () => [] },
  showSearch: { type: Boolean, default: false },
  headers: { type: Array, default: () => ["Дата", "Название", "Сумма"] },
  fetchCharts: { type: Boolean, default: false },
});

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

const categories = computed(() => categoryStore.categories);
const tags = computed(() => tagStore.tags);
const units = computed(() => unitStore.units);

const filteredItems = computed(() => {
  if (!searchQuery.value) return props.items;
  return props.items.filter((item) =>
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

async function createRecord(record) {
  await recordsStore.createRecord(record);
  formModalVisible.value = false;
}

async function updateRecord(record) {
  await recordsStore.updateRecord(record);
  formModalVisible.value = false;
  editingRecord.value = null;
  if (props.fetchCharts) {
    await fetchCharts(record);
  }
}

async function deleteRecord(record) {
  if (confirm("Вы уверены, что хотите удалить эту запись?")) {
    await recordsStore.deleteRecord(record.id);
    if (props.fetchCharts) {
      await fetchCharts(record);
    }
  }
}

async function fetchCharts(record) {
  const record_date = new Date(record.record_date);
  if (
    record_date.getMonth() + 1 == statsStore.currentChartMonth &&
    record_date.getFullYear() == statsStore.currentChartYear
  ) {
    await statsStore.fetchStats(
      record_date.getMonth() + 1,
      record_date.getFullYear()
    );
  }
}

defineExpose({ showFormModal });
</script>

<style scoped>
.table_view {
  display: flex;
  flex-direction: column;
  gap: 20px;
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
