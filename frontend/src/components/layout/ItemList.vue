<template>
    <div class="item-list">
        <h3 class="title primary">{{ title }}</h3>
        <ul>
            <li v-for="item in items" :key="item.id">
                <span class="color-badge" v-if="showColor" :style="{ backgroundColor: item.color_name }"></span>
                {{ item.name }}
                <span v-if="showDefaultValue" class="default-value">
                    ({{ item.default_value }})
                </span>
                <div class="actions">
                    <button @click="$emit('edit', item)">✏️</button>
                    <button @click="$emit('delete', item.id)">🗑️</button>
                </div>
            </li>
        </ul>
        <div class="add-form">
            <input v-model="newName" :placeholder="placeholder" @keyup.enter="handleAdd" />
            <ColorPicker v-if="showColor" v-model:pureColor="newColor" picker-type="chrome" disable-alpha
                class="color-picker" />
            <input v-if="showDefaultValue" v-model.number="newDefaultValue" type="number" min="0"
                placeholder="Значение по умолчанию" />
            <button class="add-btn" @click="handleAdd">
                Добавить
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { ColorPicker } from 'vue3-colorpicker'
import 'vue3-colorpicker/style.css'

const props = defineProps({
    title: String,
    items: Array,
    placeholder: String,
    showColor: Boolean,
    showDefaultValue: Boolean
})

const emit = defineEmits(['add', 'edit', 'delete'])

const newName = ref('')
const newColor = ref('#3ddac9')
const newDefaultValue = ref(0)

function rgbToHex(rgb) {
  if (!rgb.startsWith('rgb')) return rgb;
  const nums = rgb.match(/\d+/g);
  if (!nums) return rgb;
  return (
    '#' +
    nums
      .map(x => parseInt(x).toString(16).padStart(2, '0'))
      .join('')
      .toLowerCase()
  );
}

const handleAdd = () => {
  if (!newName.value.trim()) return;

  let color = props.showColor ? rgbToHex(newColor.value) : undefined;
  const payload = {
    category_name: newName.value.trim(),
    ...(props.showColor && { category_color: color }),
    ...(props.showDefaultValue && { default_value: newDefaultValue.value })
  };

  emit('add', payload);

  newName.value = '';
  newColor.value = '#3ddac9';
  newDefaultValue.value = 0;
}

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

.color-picker {
    width: 40px;
    height: 40px;
}

input {
    flex: 1;
    padding: 8px;
    background: #333;
    border: 1px solid #444;
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

.actions button {
    background: none;
    border: none;
    color: #888;
    cursor: pointer;
    margin-left: 8px;
}

.actions button:hover {
    color: #3ddac9;
}
</style>