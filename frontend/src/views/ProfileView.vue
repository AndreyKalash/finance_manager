<template>
  <section class="profile">
    <div class="container">
      <h2>Профиль пользователя</h2>
      <div v-if="user" class="profile-info">
        <div class="profile-card">
          <div class="avatar">
            <img :src="user.avatar || '/default-avatar.png'" alt="Аватар">
          </div>
          <div class="details">
            <p><strong>Имя пользователя:</strong> {{ user.username }}</p>
            <p><strong>Email:</strong> {{ user.email }}</p>
            <p><strong>Дата регистрации:</strong> {{ formatDate(user.created_at) }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="settings container">
      <h1 class="primary title">Списки</h1>
      <div class="crud-flex-row">
        <ItemList title="Категории" :items="mainCategories" placeholder="Новая категория" :showColor="true"
          @add="handleAddCategory" @edit="handleEditCategory" @delete="handleDeleteCategory" />

        <ItemList title="Теги" :items="tags" placeholder="Новый тег" :showColor="true" @add="handleAddTag"
          @edit="handleEditTag" @delete="handleDeleteTag" />

        <ItemList title="Единицы измерения" :items="units" placeholder="Новая единица" :showDefaultValue="true"
          @add="handleAddUnit" @edit="handleEditUnit" @delete="handleDeleteUnit" />
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCategoriesStore } from '@/stores/categories'
import { useTagsStore } from '@/stores/tags'
import { useUnitsStore } from '@/stores/units'
import ItemList from '@/components/layout/ItemList.vue'

const categoriesStore = useCategoriesStore()
const tagsStore = useTagsStore()
const unitsStore = useUnitsStore()

const user = ref(null)
const mainCategories = computed(() => categoriesStore.categories)
const tags = computed(() => tagsStore.tags)
const units = computed(() => unitsStore.units)

const handleAddCategory = async ({ name, color }) => {
  await categoriesStore.createCategory(name, color);
}

const handleEditCategory = async (item) => {
  await categoriesStore.updateCategory(item)
}

const handleDeleteCategory = async (id) => {
  if (!confirm('Удалить категорию?')) return
  await categoriesStore.deleteCategory(id)
}

const handleAddTag = async ({name, color}) => {
  await tagsStore.createTag(name, color)
}

const handleEditTag = async (item) => {
  await tagsStore.updateTag(item)
}

const handleDeleteTag = async (id) => {
  if (!confirm('Удалить тег?')) return
  await tagsStore.deleteTag(id)
}

const handleAddUnit = async ({ name, default_value }) => {
  await unitsStore.createUnit(
    name,
    Number(default_value) || 0
  )
}

const handleEditUnit = async (item) => {
  await unitsStore.updateUnit(item.id, item.name, item.default_value)
}

const handleDeleteUnit = async (id) => {
  if (!confirm('Удалить единицу измерения?')) return
  await unitsStore.deleteUnit(id)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

</script>

<style scoped>
.profile-card {
  display: flex;
  gap: 2rem;
  padding: 1.5rem;
  background: #2a2a2a;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.avatar img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #bb86fc;
}

.details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.crud-flex-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .crud-flex-row {
    grid-template-columns: 1fr;
  }

  .profile-card {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
}
</style>
