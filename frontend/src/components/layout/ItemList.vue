<template>
  <div class="item-list">
    <h3 class="title primary">{{ title }}</h3>
    <div class="add-form">
      <AppDropdown ref="dropdownRef" :items="filteredItems" :show-color="showColor" :placeholder="placeholder"
        :name-key="nameKey" :self-close="false" :color-key="colorKey" v-model="newName">
        <template #item="{ item }">
          <li class="option-item">
            <template v-if="editingId === item.id">
              <div class="edit-wrapper" ref="editWrapperRef">
                <ColorPicker v-if="!showDefaultValue" @click.stop v-model:pureColor="editColor" picker-type="chrome"
                  disable-alpha class="color-badge color-picker-inline" :style="{ backgroundColor: editColor }"
                  inline />
                <input @click.stop v-model="editName" class="edit-input" :placeholder="placeholder"
                  @keyup.enter="saveEdit(item)" autofocus />
                <input v-if="showDefaultValue" @click.stop v-model.number="editDefaultValue" class="number_input"
                  title="Значение по умолчанию" @keyup.enter="saveEdit(item)" type="number" min="1"
                  placeholder="Значение по умолчанию" />
                <div class="list-actions">
                  <button class="save-btn" @click.stop="saveEdit(item)">
                    💾
                  </button>
                  <button class="cancel-btn" @click.stop="cancelEdit">
                    ✖️
                  </button>
                </div>
              </div>
            </template>
            <template v-else>
              <div class="item-content">
                <span class="color-badge" v-if="showColor" :style="{ backgroundColor: item[colorKey] }"
                  title="Цвет"></span>
                <span class="item-text">{{ item[nameKey] }}</span>
                <span v-if="showDefaultValue" class="default-value">
                  ({{ item.default_value }})
                </span>
              </div>
              <div class="item-actions">
                <button class="edit-btn" @click.stop="startEdit(item)">
                  ✏️
                </button>
                <button class="delete-btn" @click.stop="$emit('delete', props.itemType, item.id)">
                  🗑️
                </button>
              </div>
            </template>
          </li>
        </template>
      </AppDropdown>

      <ColorPicker v-if="showColor" v-model:pureColor="newColor" picker-type="chrome" disable-alpha
        class="color-picker" />
      <input v-if="showDefaultValue" v-model.number="newDefaultValue" class="number_input"
        title="Значение по умолчанию" type="number" min="1" placeholder="Значение по умолчанию" />
      <button class="add-btn" @click="handleAdd">Добавить</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { ColorPicker } from "vue3-colorpicker";
import "vue3-colorpicker/style.css";
import AppDropdown from "./AppDropdown.vue";

const props = defineProps({
  title: String,
  items: Array,
  placeholder: String,
  showColor: Boolean,
  showDefaultValue: Boolean,
  nameKey: { type: String, default: "name" },
  colorKey: { type: String, default: "color" },
  itemType: { type: String, required: false }
});

const emit = defineEmits(["add", "edit", "delete"]);

const filteredItems = ref([]);
const dropdownRef = ref(null);
const editWrapperRef = ref(null);

const editingId = ref(null);

const newName = ref("");
const editName = ref("");

const newColor = ref("#3ddac9");
const editColor = ref("#3ddac9");

const newDefaultValue = ref(1);
const editDefaultValue = ref(1);

function resetForm() {
  newName.value = "";
  newColor.value = "#3ddac9";
  newDefaultValue.value = 1;
  dropdownRef.value?.closeDropdown();
}

const filterOptions = () => {
  if (!newName.value) {
    filteredItems.value = props.items;
  } else {
    filteredItems.value = props.items.filter(
      (item) =>
        item &&
        String(item[props.nameKey])
          .toLowerCase()
          .includes(newName.value.toLowerCase())
    );
  }
};

const startEdit = async (item) => {
  editingId.value = item.id;
  editName.value = item[props.nameKey];
  editColor.value = item[props.colorKey] || "#3ddac9";
  editDefaultValue.value = item.default_value ?? 1;
};

const saveEdit = (item) => {
  emit("edit", props.itemType, {
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

  const payload = {
    [props.nameKey]: newName.value.trim(),
    ...(props.showColor && {
      [props.colorKey]: newColor.value.startsWith("#")
        ? newColor.value
        : rgbToHex(newColor.value),
    }),
    ...(props.showDefaultValue && {
      default_value: Number(newDefaultValue.value) || 0,
    }),
  };

  if (props.itemType) {
    emit("add", props.itemType, payload);
  } else {
    emit("add", payload);
  }
  resetForm();
  dropdownRef.value.searchQuery = '';
};

const handleClickOutside = (event) => {
  const dropdownEl = dropdownRef.value?.$el || dropdownRef.value;
  const editEl = editWrapperRef?.value;

  if (
    (dropdownEl && dropdownEl.contains(event.target)) ||
    (editEl && editEl.contains(event.target)) ||
    event.target.closest(".vc-colorpicker")
  ) {
    return;
  }
  dropdownRef.value?.closeDropdown();
  cancelEdit();
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
  min-width: 18px;
  min-height: 18px;
  border-radius: 4px;
  margin-right: 8px;
  border: 1px solid #444;
  cursor: default;
}

.color-picker>>>.vc-color-wrap {
  pointer-events: none;
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

.edit-buttons {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  gap: 4px;
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
  justify-content: space-between;
  align-items: center;
  width: 100%;
  position: relative;
  min-height: 40px;
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
  margin-left: auto;
  display: flex;
  gap: 8px;
  padding-left: 16px;
}

.color-picker {
  position: absolute;
  z-index: 1001;
  width: 40px;
  height: 40px;
  top: 100%;
  left: 0;
}

.text-input {
  width: 90%;
}

.number_input {
  width: 50px;
  min-width: auto;
  -moz-appearance: textfield;
  padding: 8px;
  border: 1px solid #444;
  background: #333;
  border-radius: 4px;
  color: white;
  margin-right: 8px;
  flex-shrink: 0;
}

.number_input::-webkit-outer-spin-button,
.number_input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
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
  align-items: center;
  width: 100%;
  position: relative;
}

.add-form {
  z-index: 1;
}

.color-picker-inline :deep(.vc-color-wrap),
.color-picker-inline :deep(.vc-color-wrap__trigger) {
  width: 18px !important;
  height: 18px !important;
  min-width: 18px !important;
  min-height: 18px !important;
  border-radius: 4px !important;
  box-shadow: none !important;
  padding: 0 !important;
}
</style>
