<template>
  <div class="modal" v-if="modelValue">
    <div class="modal-content">
      <h3>{{ isEditing ? 'Редактировать' : 'Добавить' }} запись</h3>
      <form @submit.prevent="submitForm">
        <label for="record-date">Дата</label>
        <input id="record-date" v-model="formData.record_date" type="date" required />

        <label for="record-name">Название</label>
        <input id="record-name" v-model="formData.name" type="text" placeholder="Название" required />

        <label for="record-price">Цена</label>
        <input id="record-price" v-model.number="formData.price" type="number" step="0.01" placeholder="Цена" required />

        <label for="record-unit">Единица измерения</label>
        <select id="record-unit" v-model="formData.unit_id" required>
          <option disabled value="" hidden>Выберите единицу</option>
          <option v-for="unit in units" :key="unit.id" :value="unit.id">
            {{ unit.name }}
          </option>
        </select>

        <label for="record-unit-quantity">Количество единиц измерения</label>
        <input id="record-unit-quantity" v-model.number="formData.unit_quantity" type="number"
          placeholder="Кол-во ед." required />

        <label for="record-product-quantity">Количество товара</label>
        <input id="record-product-quantity" v-model.number="formData.product_quantity" type="number"
          placeholder="Кол-во товара" required />

        <label for="record-category">Категория</label>
        <div class="custom-select">
          <select id="record-category" v-model="formData.category_id" required>
            <option disabled value="" hidden>Выберите категорию</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
          <div class="color-box" v-if="selectedCategory" 
            :style="{ backgroundColor: selectedCategory.color }"></div>
        </div>

        <label for="record-tags">Теги</label>
        <div class="tags-container">
          <select id="record-tags" v-model="formData.tags" multiple>
            <option v-for="tag in tags" :key="tag.id" :value="tag.id">
              {{ tag.name }}
            </option>
          </select>
          <div class="selected-tags">
            <div v-for="tag in formData.tags" :key="tag" class="tag-item">
              <div class="color-box" :style="{ backgroundColor: getTagColor(tag) }"></div>
              <span>{{ getTagName(tag) }}</span>
            </div>
          </div>
        </div>

        <div class="modal-actions">
          <button type="submit" class="add_row_btn">{{ isEditing ? 'Сохранить' : 'Добавить' }}</button>
          <button type="button" class="add_row_btn" @click="$emit('update:modelValue', false)">Отмена</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  modelValue: Boolean,
  recordToEdit: Object,
  categories: Array,
  tags: Array,
  units: Array
});

const emit = defineEmits(['update:modelValue', 'create', 'update']);

const formData = ref(getEmptyRecord());

function getEmptyRecord() {
  return {
    record_date: new Date().toISOString().split('T')[0],
    name: '',
    price: 0,
    unit_quantity: 1,
    product_quantity: 1,
    unit_id: '',
    category_id: '',
    tags: []
  }
}

const isEditing = computed(() => !!props.recordToEdit);

const selectedCategory = computed(() => {
  if (!formData.value.category_id) return null;
  return props.categories.find(cat => cat.id === formData.value.category_id);
});

function getTagColor(tagId) {
  const tag = props.tags.find(t => t.id === tagId);
  return tag ? tag.color : '#808080';
}

function getTagName(tagId) {
  const tag = props.tags.find(t => t.id === tagId);
  return tag ? tag.name : '';
}

function submitForm() {
  if (isEditing.value) {
    emit('update', { ...formData.value });
  } else {
    emit('create', { ...formData.value });
  }
}

watch(() => props.recordToEdit, (newVal) => {
  if (newVal) {
    formData.value = { ...newVal };
  } else {
    formData.value = getEmptyRecord();
  }
}, { immediate: true });

watch(() => props.modelValue, (visible) => {
  if (!visible && !props.recordToEdit) {
    formData.value = getEmptyRecord();
  }
});
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.modal-content {
  background: #232323;
  padding: 30px 20px;
  border-radius: 10px;
  min-width: 400px;
  max-width: 500px;
  color: #e0e0e0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.modal-content input,
.modal-content select {
  width: 95%;
  padding: 8px;
  margin-bottom: 8px;
  background: #2b2b2b;
  border: 1px solid #bb86fc;
  border-radius: 5px;
  color: #d9cfcf;
}

.modal-content label {
  margin-top: 8px;
  margin-bottom: 2px;
  color: #bb86fc;
  font-size: 15px;
  display: block;
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.add_row_btn {
  padding: 10px 20px;
  border: none;
  background-color: #03dac6;
  color: #121212;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-family: 'Roboto', monospace;
  margin-top: 10px;
}

.color-box {
  width: 16px;
  height: 16px;
  border-radius: 3px;
  display: inline-block;
  margin-right: 5px;
  vertical-align: middle;
}

.custom-select {
  display: flex;
  align-items: center;
  position: relative;
}

.custom-select .color-box {
  position: absolute;
  right: 30px;
  pointer-events: none;
}

.tags-container {
  margin-bottom: 10px;
}

.selected-tags {
  margin-top: 5px;
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.tag-item {
  background: #333;
  padding: 3px 8px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  font-size: 0.9em;
}
</style>
