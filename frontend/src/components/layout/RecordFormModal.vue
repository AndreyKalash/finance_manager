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
        <input id="record-price" v-model.number="formData.price" type="number" step="0.01" placeholder="Цена"
          required />

        <label for="record-unit">Единица измерения</label>
        <AppDropdown ref="unitDropdown" @select="handleUnitSelect" v-model="formData.unit_id" :show-color="false"
          :items="units" placeholder="Выберите единицу" name-key="name" class="dropdown">
          <template #item="{ item }">
            <div>
              <span>{{ item.name }}</span>
              <span class="default-value">({{ item.default_value }})</span>
            </div>
          </template>
        </AppDropdown>

        <label for="record-unit-quantity">Количество единиц измерения</label>
        <input id="record-unit-quantity" v-model.number="formData.unit_quantity" type="number"
          placeholder="Кол-во ед." />

        <label for="record-product-quantity">Количество товара</label>
        <input id="record-product-quantity" v-model.number="formData.product_quantity" type="number"
          placeholder="Кол-во товара" />

        <label>Категория</label>
        <AppDropdown
          ref="categoryDropdown"
          @select="handleCategorySelect"
          v-model="formData.category_id"
          :show-color="true"
          :items="categories"
          placeholder="Выберите категорию"
          name-key="name" class="dropdown"
        >
        </AppDropdown>

        <label>Теги</label>
        <div class="tags-container">
          <div class="tags-list">
            <div v-for="tag in tags" :key="tag.id" class="tag-option"
              :class="{ 'selected': formData.tags.includes(tag.id) }" @click="toggleTag(tag.id)">
              <div class="color-box" :style="{ backgroundColor: tag.color }"></div>
              <span>{{ tag.name }}</span>
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
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import AppDropdown from './AppDropdown.vue';

const props = defineProps({
  modelValue: Boolean,
  recordToEdit: Object,
  categories: Array,
  tags: Array,
  units: Array
});

const emit = defineEmits(['update:modelValue', 'create', 'update']);

const formData = ref(getEmptyRecord());
const isCategoryOpen = ref(false);
const categoryDropdown = ref(null);
const unitDropdown = ref(null)

function getEmptyRecord() {
  return {
    id: '',
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

const handleUnitSelect = (unit) => {
  formData.value.unit_id = unit.id;
  formData.value.unit_quantity = unit.default_value
  unitDropdown.value.closeDropdown();
};

function handleCategorySelect(category) {
  formData.value.category_id = category.id;
  categoryDropdown.value.closeDropdown();
  isCategoryOpen.value = false;
}

function toggleTag(tagId) {
  const index = formData.value.tags.indexOf(tagId);
  if (index === -1) {
    formData.value.tags.push(tagId);
  } else {
    formData.value.tags.splice(index, 1);
  }
}

function submitForm() {
  if (isEditing.value) {
    emit('update', { ...formData.value });
  } else {
    emit('create', { ...formData.value });
  }
}

const handleClickOutside = (event) => {
  if (!props.modelValue) return;
  
  const categoryEl = categoryDropdown.value?.$el;
  const unitEl = unitDropdown.value?.$el;
  
  if (
    (categoryEl && categoryEl.contains(event.target)) ||
    (unitEl && unitEl.contains(event.target))
  ) {
    return;
  }
  
  categoryDropdown.value?.closeDropdown();
  unitDropdown.value?.closeDropdown();
};


onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});

watch(
  () => props.recordToEdit,
  (newVal) => {
    if (newVal) {
      formData.value = {
        id: newVal.id || '',
        record_date: newVal.record_date,
        name: newVal.name,
        price: Number(newVal.price),
        unit_quantity: Number(newVal.unit_quantity),
        product_quantity: Number(newVal.product_quantity),
        unit_id: newVal.unit?.id || '',
        category_id: newVal.category?.id || '',
        tags: Array.isArray(newVal.tags) ? newVal.tags.map(t => t.id) : []
      }
    } else {
      formData.value = getEmptyRecord();
    }
  },
  { immediate: true }
);

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

input,
select,
.dropdown input {
  width: 95%;
  padding: 8px;
  margin-bottom: 8px;
  background: #2b2b2b;
  border: 1px solid #bb86fc;
  border-radius: 5px;
  color: #d9cfcf;
  transition: border-color 0.3s ease;
  font-size: 14px;
}

input:focus,
.dropdown input:focus {
  border-color: #03dac6;
  outline: none;
}

label {
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
  margin-top: 10px;
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
}

.color-box {
  width: 16px;
  height: 16px;
  border-radius: 3px;
  display: inline-block;
  margin-right: 5px;
  vertical-align: middle;
}

.tags-container {
  margin-bottom: 10px;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-option {
  padding: 4px 8px;
  border: 1px solid #444;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s;
}

.tag-option.selected {
  border-color: #bb86fc;
  background: #3a3a3a;
}

.dropdown {
  position: relative;
  width: 100%;
  margin-bottom: 1rem;
}

.dropdown .dropdown-content {
  width: 95%;
  left: 2.5%;
  background: #2b2b2b;
  border-color: #bb86fc;
}

.dropdown .default-value {
  color: #888;
  margin-left: 8px;
  font-size: 0.9em;
}
</style>
