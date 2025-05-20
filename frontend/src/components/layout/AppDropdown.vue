<template>
  <div class="dropdown-wrapper" ref="dropdownRef">
    <input v-if="props.search"
      class="dropdown-input"
      :placeholder="placeholder"
      v-model="searchQuery"
      @focus="isOpen = true"
    />
    <input v-else
      class="dropdown-input"
      :placeholder="placeholder"
      :value ="modelValue"
      v-model="searchQuery"
      @focus="isOpen = true"
      @input="handleInput"
    />

    <div class="dropdown-content" v-show="isOpen">
      <ul class="options-list">
        <li
          v-for="item in filteredItems"
          :key="item.id"
          class="option-item"
          @click.stop="handleItemClick(item)"
        >
          <slot name="item" :item="item">
            <div class="default-item">
              <span
                v-if="showColor"
                class="color-badge"
                :style="{ backgroundColor: item[colorKey] }"
              ></span>
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
// eslint-disable-next-line no-unused-vars
import { ref, computed, watch } from "vue";

const props = defineProps({
  items: Array,
  placeholder: String,
  showColor: Boolean,
  nameKey: { type: String, default: "name" },
  colorKey: { type: String, default: "color" },
  modelValue: [String, Number, Array],
  search: { type: Boolean, default: false}
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

const handleInput = (event) => {
  const value = event.target.value
  searchQuery.value = value;
  emit("update:modelValue", value);
}

const handleItemClick = (item) => {
  emit("select", item);
};

function closeDropdown() {
  isOpen.value = false;
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
