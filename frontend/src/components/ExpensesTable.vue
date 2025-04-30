<template>
  <div class="table_view">
    <div class="search" v-if="showSearch">
      <i class="fa-solid fa-magnifying-glass secondary"></i>
      <input type="search" v-model="searchQuery" placeholder="Поиск по таблице">
    </div>

    <div class="table_container" @mouseenter="onTableMouseEnter" @mouseleave="onTableMouseLeave">
  <table class="expenses_table">
    <thead>
      <tr>
        <th v-for="header in headers" :key="header">{{ header }}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, index) in filteredItems" :key="index">
        <td>{{ item.date }}</td>
        <td>{{ item.name }}</td>
        <td>{{ item.price }}</td>
        <!-- остальные поля -->
        <td class="modify">
          <button class="mbtn" @click="$emit('edit', item)">✎</button>
          <button class="mbtn" @click="$emit('delete', item)">🗑</button>
        </td>
      </tr>
      <!-- Плюсовая строка -->
      <tr
        class="plus-row"
        v-if="tableHover || plusRowHover"
        @mouseenter="onPlusRowMouseEnter"
        @mouseleave="onPlusRowMouseLeave"
      >
        <td :colspan="headers.length" class="plus-cell">
          <span class="plus-btn" @click="$emit('add-row')">+</span>
        </td>
      </tr>
    </tbody>
  </table>
</div>


  </div>
</template>

<script setup>
import { computed, ref } from 'vue';

const props = defineProps({
  items: Array,
  showSearch: Boolean,
  headers: Array
});

const searchQuery = ref('');
const plusRowHover = ref(false);
const tableHover = ref(false);

const filteredItems = computed(() => {
  return props.items.filter(item =>
    item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

function onTableMouseEnter() {
  tableHover.value = true;
}
function onTableMouseLeave() {
  tableHover.value = false;
}
function onPlusRowMouseEnter() {
  plusRowHover.value = true;
}
function onPlusRowMouseLeave() {
  plusRowHover.value = false;
}

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

#expenses_search {
  padding: 5px;
  width: 100%;
  background-color: #2b2b2b;
  border: 1px solid #bb86fc;
  border-radius: 5px;
  color: #d9cfcf;
}

#expenses_search:hover {
  background-color: #333;
}

#expenses_search:focus {
  outline: none;
  box-shadow: none;
  border-color: #03dac6;
}

.fa-magnifying-glass {
  font-size: 20px;
  margin-right: 15px;
}

.expenses_table {
  width: 100%;
  border-collapse: collapse;

}

.expenses_table tr {
  text-align: center;
}

.expenses_table th {
  background-color: #333;
  color: #f5f5f5;
  font-weight: bold;
  padding: 10px;
  border: 1px solid #444;

}

.expenses_table td {
  color: #e0e0e0;
  padding: 10px;
  border: 1px solid #444;

}

.expenses_table tr:nth-child(odd) {
  background-color: #2a2a2a;
}

.expenses_table tr:nth-child(even) {
  background-color: #1e1e1e;
}

.expenses_table tr:hover {
  background-color: #333;
}

.new_row td {
  text-align: center;
  padding: 5px;
}

.new_row input,
.new_row select {
  width: 100%;
  padding: 5px;

  color: #d9cfcf;
  background-color: transparent;
  border: 1px solid #444;
  border-radius: 4px;
  box-sizing: border-box;

  outline: none;
  font-family: 'Roboto', monospace;
  font-size: 16px;
  text-align: center;

  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  position: relative;

}

input[type='number'] {
  appearance: none;
  -moz-appearance: textfield;
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
}

.fa-pen {
  color: #03dac6;
}

.fa-trash {
  color: #cf6679;
}

.mbtn {
  background: none;
  border: none;
  cursor: pointer;
  color: #bb86fc;
  font-size: 18px;
  padding: 5px;
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
  font-family: 'Roboto', monospace;
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