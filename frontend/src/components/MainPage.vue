<template>
    <main class="main">
      <div class="expenses_chart_items">
        <ChartSection type="sum" />
        <ChartSection type="count" />
      </div>
  
      <ExpensesTable
        :items="expenses"
        :headers="tableHeaders"
        @edit="handleEdit"
        @delete="handleDelete"
      />
    </main>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import ExpensesTable from './ExpensesTable.vue';
  import ChartSection from './ChartSection.vue';
  
  const tableHeaders = ref([
    'Дата', 'Название', 'Цена товара', 'Единица измерения', 
    'Количество единицы измерения', 'Количество товара', 
    'Категория', 'Подкатегории', 'Действия'
  ]);
  
  const expenses = ref([1, 2, 3]); // Данные из API
  
//   const handleEdit = (item) => {
//     // Редактирование
//   };
  
//   const handleDelete = (item) => {
//     // Удаление
//   };
  </script>
  
  <style scoped>
  @import './assets/main.css';
  </style>