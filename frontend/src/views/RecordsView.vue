<!-- RecordsView.vue -->
<template>
  <section class="records container">
    <div class="table_view">
      <div class="search">
        <i class="fa-solid fa-magnifying-glass secondary"></i>
        <!-- Поле ввода с двусторонним связыванием для поиска -->
        <input type="search" v-model="searchQuery" placeholder="Поиск по таблице" id="records_search" />
      </div>
      <!-- Компонент таблицы с передачей отфильтрованных данных -->
      <RecordsTable ref="recordsTableRef" :items="filteredRecords" :v-model="currentType"
        @update:modelValue="handleTypeChange" />
      <!-- Блок кнопок действий -->
      <div class="buttons">
        <button class="row_btn secondary" @click="showAddForm">
          Добавить запись
        </button>
        <!-- Кнопка открытия модалки экспорта -->
        <button class="row_btn secondary" @click="isExportModalOpen = true">
          <i class="fa-solid fa-file-export"></i>
          Экспорт
        </button>
      </div>
      <!-- Модальное окно экспорта -->
      <div v-if="isExportModalOpen" class="export-modal">
        <div class="modal-content">
          <span class="close" @click="isExportModalOpen = false">&times;</span>
          <h3>Выберите формат экспорта</h3>
          <div class="file-types">
            <button v-for="type in exportTypes" :key="type" @click="selectedFileType = type"
              :class="{ active: selectedFileType === type }">
              {{ type.toUpperCase() }}
            </button>
          </div>
          <button class="export-confirm" @click="handleExport" :disabled="!selectedFileType">
            Сформировать отчёт
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useCategoriesStore } from "@/stores/categories";
import { useTagsStore } from "@/stores/tags";
import { useUnitsStore } from "@/stores/units";
import { useRecordsStore } from "@/stores/records";
import RecordsTable from "@/components/RecordsTable.vue";
import { RTYPES } from "@/utils/recordTypes.js";

const categoryStore = useCategoriesStore();
const tagStore = useTagsStore();
const unitStore = useUnitsStore();
const recordsStore = useRecordsStore();
const recordsTableRef = ref(null);

const searchQuery = ref("");
const currentType = ref(RTYPES.expense);

const isExportModalOpen = ref(false);
const selectedFileType = ref(null);
const exportTypes = ref(['xlsx', 'csv', 'pdf']);

const filteredRecords = computed(() => {
  if (!searchQuery.value) return recordsStore.records[currentType.value];
  return recordsStore.records[currentType.value]?.filter(
    (record) =>
      (record.name ?? "")
        .toLowerCase()
        .includes(searchQuery.value.toLowerCase()) ||
      (record.category?.name ?? "")
        .toLowerCase()
        .includes(searchQuery.value.toLowerCase())
  );
});
// Обработчик экспорта данных
const handleExport = async () => {
  try {
    await recordsStore.exportRecords(currentType.value, selectedFileType.value)
    isExportModalOpen.value = false;
    selectedFileType.value = null;
  } catch (error) {
    console.error('Ошибка при экспорте:', error);
  }
};

function handleTypeChange(type) {
  currentType.value = type;
}

function showAddForm() {
  recordsTableRef.value?.showFormModal();
}

onMounted(async () => {
  await Promise.all([
    categoryStore.fetchCategories(),
    tagStore.fetchTags(),
    unitStore.fetchUnits(),
    recordsStore.fetchRecords(),
  ]);
});
</script>

<style scoped>
.table_view {
  display: flex;
  flex-direction: column;
  margin: 20px 0px;
}

.buttons {
  display: inline-flex;
  align-items: center;
  justify-content: space-between;
}

.search {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
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

.row_btn {
  padding: 10px 20px;
  border: none;
  background-color: #03dac6;
  color: #121212;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-family: "Roboto", monospace;
  margin-top: 10px;
  transition: background 0.3s ease;
}

.row-btn:hover {
  background-color: #018786;
}

.export-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #2b2b2b;
  padding: 2rem;
  border-radius: 8px;
  min-width: 400px;
  position: relative;
}

.close {
  position: absolute;
  right: 1rem;
  top: 1rem;
  font-size: 24px;
  cursor: pointer;
  color: #fff;
}

.file-types {
  display: flex;
  gap: 1rem;
  margin: 1.5rem 0;
}

.file-types button {
  flex: 1;
  padding: 0.8rem;
  background: #333;
  border: none;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.file-types button.active {
  background: #03dac6;
  color: #121212;
}

.export-confirm {
  width: 100%;
  padding: 12px;
  background: #03dac6;
  color: #121212;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.export-confirm:disabled {
  background: #616161;
  cursor: not-allowed;
}
</style>
