<template>
  <section class="records container">
    <div class="table_view">
      <div class="search">
        <i class="fa-solid fa-magnifying-glass secondary"></i>
        <input
          type="search"
          v-model="searchQuery"
          placeholder="Поиск по таблице"
          id="records_search"
        />
      </div>

      <RecordsTable
        ref="recordsTableRef"
        :items="filteredRecords"
        :v-model="currentType"
        @update:modelValue="handleTypeChange"
      />

      <button class="add_row_btn secondary" @click="showAddForm">
        Добавить запись
      </button>
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
  margin: 20px 0px ;
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

.add_row_btn {
  align-self: flex-start;
  padding: 10px 20px;
  border: none;
  background-color: #03dac6;
  color: #121212;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-family: "Roboto", monospace;
  margin-top: 10px;
}
</style>
