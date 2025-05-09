<template>
  <div class="table_view">
    <div class="search" v-if="showSearch">
      <i class="fa-solid fa-magnifying-glass secondary"></i>
      <input
        type="search"
        v-model="searchQuery"
        placeholder="Поиск по таблице"
        id="records_search"
      >
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
            <td>{{ item.category.name }}</td>
            <td><span v-for="(tag, index) in item.tags" :key="index">{{ tag.name }}</span></td>
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
import { computed, ref } from 'vue';
import RecordFormModal from './layout/RecordFormModal.vue';
import { useCategoriesStore } from '@/stores/categories';
import { useTagsStore } from '@/stores/tags';
import { useUnitsStore } from '@/stores/units';
import { useRecordsStore } from '@/stores/records';

const props = defineProps({
  items: {
    type: Array,
    default: () => [],
  },
  showSearch: {
    type: Boolean,
    default: false,
  },
  headers: {
    type: Array,
    default: () => ['Дата', 'Название', 'Сумма'],
  }
});

const categoryStore = useCategoriesStore();
const tagStore = useTagsStore();
const unitStore = useUnitsStore();
const recordsStore = useRecordsStore();

const searchQuery = ref('');
const tableHover = ref(false);
const formModalVisible = ref(false);
const editingRecord = ref(null);

const categories = computed(() => categoryStore.categories);
const tags = computed(() => tagStore.tags);
const units = computed(() => unitStore.units);

const filteredItems = computed(() => {
  if (!searchQuery.value) return props.items;
  return props.items.filter(item =>
    (item.name ?? '').toLowerCase().includes(searchQuery.value.toLowerCase())
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
}

async function deleteRecord(record) {
  if (confirm('Вы уверены, что хотите удалить эту запись?')) {
    await recordsStore.deleteRecord(record.id);
  }
}
defineExpose({ showFormModal })
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

.plus-row .plus-cell {
  text-align: center;
  padding: 0;
  background: #232323;
}

.plus-btn {
  display: inline-block;
  font-size: 28px;
  color: #03dac6;
  background: #222;
  border: 2px solid #03dac6;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  line-height: 32px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  user-select: none;
}
.plus-btn:hover {
  background: #03dac6;
  color: #222;
}
</style>
