<!-- AppDropdown.vue -->
<template>
  <div class="dropdown-wrapper" ref="dropdownRef">
    <!-- Условный рендеринг поля ввода в зависимости от режима поиска -->
    <input v-if="props.search" class="dropdown-input" :placeholder="placeholder" v-model="searchQuery"
      @focus="isOpen = true" />
    <!-- Базовый инпут без поиска с прямой привязкой значения -->
      <input v-else class="dropdown-input" :placeholder="placeholder" :value="modelValue" v-model="searchQuery"
      @focus="isOpen = true" @input="handleInput" />
    <!-- Контейнер выпадающего списка с управляемой видимостью -->
    <div class="dropdown-content" v-show="isOpen">
      <ul class="options-list">
        <!-- Рендеринг отфильтрованных элементов списка -->
        <li v-for="item in filteredItems" :key="item.id" class="option-item"
          :class="{ selected: props.multiple && isSelected(item) }" @click.stop="handleItemClick(item)">
          <slot name="item" :item="item">
            <div class="default-item">
              <span v-if="showColor" class="color-badge" :style="{ backgroundColor: item[colorKey] }"></span>
              <span class="item-text">{{ item[nameKey] }}</span>
            </div>
          </slot>
        </li>
        <li v-if="filteredItems.length === 0" class="option-item empty">
          Нет результатов
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from "vue";

const props = defineProps({
  items: Array,
  placeholder: String,
  showColor: Boolean,
  nameKey: { type: String, default: "name" },
  colorKey: { type: String, default: "color" },
  modelValue: [String, Number, Array],
  search: { type: Boolean, default: false },
  multiple: { type: Boolean, default: false },
  selfClose: { type: Boolean, default: true },

});

const emit = defineEmits(["update:modelValue", "select"]);

const searchQuery = ref('');
const isOpen = ref(false);
const dropdownRef = ref(null);


const filteredItems = computed(() => {
  if (!props.items) return [];
  return props.items.filter((item) =>
    item[props.nameKey]?.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});
// Обработчик ввода для обычного режима
const handleInput = (event) => {
  const value = event.target.value
  searchQuery.value = value;
  emit("update:modelValue", value);
}
// Обработчик выбора элемента
const handleItemClick = (item) => {
  if (props.multiple) {
    const newValue = props.modelValue.includes(item.id)
      ? props.modelValue.filter((id) => id !== item.id)
      : [...props.modelValue, item.id];
    emit("update:modelValue", newValue);
  }
  emit("select", item);
};

const isSelected = (item) => {
  if (props.multiple) {
    return props.modelValue.includes(item.id);
  }
  return props.modelValue === item.id;
};

function closeDropdown() {
  isOpen.value = false;
}
// Обработчик клика вне компонента
const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false;
  }
};
if (props.selfClose) {
  onMounted(() => {
    document.addEventListener("click", handleClickOutside);
  });
  onBeforeUnmount(() => {
    document.removeEventListener("click", handleClickOutside);
  });
}

defineExpose({
  closeDropdown,
  searchQuery
});

watch(
  () => props.modelValue,
  (newVal) => {
    if (!props.items && props.search) return;
    const selected = props.items.find((item) => item.id === newVal);
    searchQuery.value += selected ? selected[props.nameKey] : "";
  },
  { immediate: true }
);

</script>

<style scoped>
.dropdown-wrapper {
  position: relative;
  width: 100%;
}

.dropdown-input {
  width: 90%;
  padding: 8px;
  border: 1px solid #444;
  border-radius: 4px;
  background: #333;
  color: white;
}

.dropdown-content {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background: #333;
  border: 1px solid #444;
  border-radius: 4px;
  margin-top: 4px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
  transition: opacity 0.2s, transform 0.2s;
}

.option-item.selected {
  background: #444 !important;
  position: relative;
}

.option-item.selected::after {
  content: "✓";
  position: absolute;
  right: 12px;
  color: #03dac6;
}

.option-item:hover:not(.selected) {
  background: #373737;
}

.options-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.option-item {
  padding: 8px 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.option-item:hover {
  background: #444;
}

.color-badge {
  width: 16px;
  height: 16px;
  border-radius: 3px;
  display: inline-block;
}

.default-item {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.dropdown-content {
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}
</style>
