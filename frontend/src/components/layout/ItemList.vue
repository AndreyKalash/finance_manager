<template>
  <div class="item-list">
    <h3 class="title primary">{{ title }}</h3>
    <div class="add-form">
      <div class="combobox-wrapper" ref="comboboxRef">
        <input
          class="text-input"
          ref="editInput"
          v-model="newName"
          :placeholder="placeholder"
          @input="filterOptions"
          @focus="showDropdown = true"
        />
        <div class="dropdown" v-show="showDropdown">
          <ul class="options-list">
            <li
              v-for="item in filteredItems"
              :key="item.id"
              class="option-item"
            >
              <template v-if="editingId === item.id">
                <div class="edit-wrapper">
                  <input
                    v-model="editName"
                    class="edit-input"
                    :placeholder="placeholder"
                    @keyup.enter="saveEdit(item)"
                    autofocus
                  />
                  <ColorPicker
                    v-if="showColor"
                    v-model:pureColor="editColor"
                    picker-type="chrome"
                    disable-alpha
                    class="color-picker"
                  />
                  <input
                    v-if="showDefaultValue"
                    v-model.number="editDefaultValue"
                    class="number_input"
                    @keyup.enter="saveEdit(item)"
                    step="0.01"
                    type="number"
                    min="0"
                    placeholder="Значение по умолчанию"
                  />
                  <div class="edit-buttons">
                    <button class="save-btn" @click.stop="saveEdit(item)">💾</button>
                    <button class="cancel-btn" @click.stop="cancelEdit">✖️</button>
                  </div>
                </div>
              </template>
              <template v-else>
                <div class="item-content">
                  <span
                    class="color-badge"
                    v-if="showColor"
                    :style="{ backgroundColor: item[colorKey] || '#000000' }"
                    title="Цвет"
                  ></span>
                  <span class="item-text">{{ item[nameKey] }}</span>
                  <span v-if="showDefaultValue" class="default-value">
                    ({{ item.default_value }})
                  </span>
                </div>
                <div class="item-actions">
                  <button class="edit-btn" @click.stop="startEdit(item)">✏️</button>
                  <button class="delete-btn" @click.stop="$emit('delete', item.id)">🗑️</button>
                </div>
              </template>
            </li>
            <li v-if="filteredItems.length === 0" class="option-item empty">
              Нет записей
            </li>
          </ul>
        </div>
      </div>
      <ColorPicker
        v-if="showColor"
        v-model:pureColor="newColor"
        picker-type="chrome"
        disable-alpha
        class="color-picker"
      />
      <input
        v-if="showDefaultValue"
        v-model.number="newDefaultValue"
        class="number_input"
        step="0.01"
        type="number"
        min="0"
        placeholder="Значение по умолчанию"
      />
      <button class="add-btn" @click="handleAdd">Добавить</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { ColorPicker } from "vue3-colorpicker";
import "vue3-colorpicker/style.css";

const props = defineProps({
  title: String,
  items: Array,
  placeholder: String,
  showColor: Boolean,
  showDefaultValue: Boolean,
  nameKey: { type: String, default: "name" },
  colorKey: { type: String, default: "color" },
});

const emit = defineEmits(["add", "edit", "delete"]);

const newName = ref("");
const newColor = ref("#3ddac9");
const newDefaultValue = ref(0);
const showDropdown = ref(false);
const filteredItems = ref([]);

const editingId = ref(null);
const editName = ref("");
const editColor = ref("#3ddac9");
const editDefaultValue = ref(0);

const comboboxRef = ref(null);

const filterOptions = () => {
  if (!newName.value) {
    filteredItems.value = props.items;
  } else {
    filteredItems.value = props.items.filter(
      (item) =>
        item &&
        String(item[props.id])
          .toLowerCase()
          .includes(newName.value.toLowerCase())
    );
  }
};

const startEdit = async (item) => {
  editingId.value = item.id;
  editName.value = item[props.nameKey];
  editColor.value = item[props.colorKey] || "#3ddac9";
  editDefaultValue.value = item.default_value ?? 0;
};

const saveEdit = (item) => {
  emit("edit", {
    ...item,
    [props.nameKey]: editName.value,
    ...(props.showColor && { [props.colorKey]: rgbToHex(editColor.value) }),
    ...(props.showDefaultValue && { default_value: editDefaultValue.value }),
  });
  cancelEdit();
};

const cancelEdit = () => {
  editingId.value = null;
};

function rgbToHex(rgb) {
  if (!rgb.startsWith("rgb")) return rgb;
  const nums = rgb.match(/\d+/g);
  if (!nums) return rgb;
  return (
    "#" +
    nums
      .map((x) => parseInt(x).toString(16).padStart(2, "0"))
      .join("")
      .toLowerCase()
  );
}

const handleAdd = () => {
  if (!newName.value.trim()) return;
  let color = props.showColor ? rgbToHex(newColor.value) : undefined;
  const payload = {
    [props.nameKey]: newName.value.trim(),
    ...(props.showColor && { [props.colorKey]: color }),
    ...(props.showDefaultValue && { default_value: newDefaultValue.value }),
  };
  emit("add", payload);
  setTimeout(() => {
    filterOptions();
  }, 0);
  newName.value = "";
  newColor.value = "#3ddac9";
  newDefaultValue.value = 0;
  showDropdown.value = false;
};

const handleClickOutside = (event) => {
  if (
    comboboxRef.value &&
    !comboboxRef.value.contains(event.target) &&
    !editingId.value
  ) {
    showDropdown.value = false;
  }
};

onMounted(() => {
  filterOptions();
  document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});

watch(
  () => [...props.items],
  () => {
    filterOptions();
  },
  { deep: true }
);
</script>

<style scoped>
.item-list {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
}

.color-badge {
  display: inline-block;
  width: 18px;
  height: 18px;
  border-radius: 4px;
  margin-right: 8px;
  border: 1px solid #444;
  cursor: default;
}

.default-value {
  color: #888;
  margin-left: 8px;
  font-size: 0.9em;
}

.add-form {
  display: flex;
  gap: 8px;
  margin-top: 1rem;
  align-items: center;
}

.combobox-wrapper {
  position: relative;
  flex: 1;
}

.dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background: #333;
  border: 1px solid #444;
  border-radius: 4px;
  margin-top: 4px;
  max-height: 240px;
  overflow-y: auto;
  z-index: 10;
}

.options-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.option-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 8px 12px;
  cursor: pointer;
}

.option-item:hover {
  background: #444;
}

.option-item.empty {
  color: #888;
  font-style: italic;
}

.item-content {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1 1 0;
  min-width: 0;
  overflow: hidden;
}

.item-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-actions {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-left: auto;
}

.color-picker {
  width: 40px;
  height: 40px;
  border: 1px solid #444;
}

.text-input {
  width: 90%;
}

.number_input {
  width: 7ch !important; 
  max-width: 100%;
  min-width: 4ch;
  box-sizing: content-box;
  padding: 8px;
  border: 1px solid #444;
  background: #333;
  border-radius: 4px;
  color: white;
  margin-right: 8px;
}

@media (max-width: 600px) {
  .number_input {
    width: 6ch !important;
  }
}
input {
  padding: 8px;
  border: 1px solid #444;
  background: #333;
  border-radius: 4px;
  color: white;
}

.add-btn {
  background: #3ddac9;
  color: #121212;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.add-btn:hover {
  opacity: 0.9;
}

.edit-input {
  flex: 1;
  padding: 6px;
  border: 1px solid #888;
  border-radius: 4px;
  background: #222;
  color: #fff;
  margin-right: 4px;
}

.save-btn,
.cancel-btn,
.edit-btn,
.delete-btn {
  background: none;
  border: none;
  color: #bb86fc;
  cursor: pointer;
  font-size: 1.1em;
  margin-left: 2px;
}

.save-btn:hover,
.edit-btn:hover {
  color: #03dac6;
}

.cancel-btn:hover,
.delete-btn:hover {
  color: #cf6679;
}

.edit-wrapper {
  display: flex;
  gap: 8px;
  align-items: center;
  width: 100%;
}
</style>
