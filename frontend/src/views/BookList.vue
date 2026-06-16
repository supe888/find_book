<template>
  <div class="page-container book-list-page">
    <div class="page-header">
      <h1>全部图书</h1>
      <p>共 {{ total }} 本电子书</p>
    </div>

    <div class="filter-bar card">
      <el-input
        v-model="keyword"
        placeholder="搜索书名、作者..."
        clearable
        style="width: 280px"
        @clear="fetchBooks"
        @keyup.enter="fetchBooks"
      >
        <template #prefix><el-icon><Search /></el-icon></template>
      </el-input>

      <el-select
        v-model="categoryId"
        placeholder="全部分类"
        clearable
        style="width: 160px"
        @change="handleFilterChange"
      >
        <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
      </el-select>

      <el-button type="primary" @click="fetchBooks">搜索</el-button>
    </div>

    <div v-loading="loading" class="book-grid">
      <BookCard v-for="book in books" :key="book.id" :book="book" />
      <el-empty v-if="!loading && books.length === 0" description="暂无图书" />
    </div>

    <div v-if="total > pageSize" class="pagination">
      <el-pagination
        v-model:current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        background
        @current-change="fetchBooks"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api, type Book, type Category } from '@/api'
import BookCard from '@/components/BookCard.vue'

const route = useRoute()
const router = useRouter()

const books = ref<Book[]>([])
const categories = ref<Category[]>([])
const loading = ref(false)
const keyword = ref('')
const categoryId = ref<number | undefined>()
const page = ref(1)
const pageSize = 12
const total = ref(0)

function handleFilterChange() {
  page.value = 1
  fetchBooks()
}

async function fetchBooks() {
  loading.value = true
  try {
    const res = await api.getBooks({
      page: page.value,
      page_size: pageSize,
      keyword: keyword.value || undefined,
      category_id: categoryId.value,
    })
    books.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  keyword.value = (route.query.keyword as string) || ''
  categoryId.value = route.query.category_id ? Number(route.query.category_id) : undefined
  categories.value = await api.getCategories()
  await fetchBooks()
})

watch([keyword, categoryId, page], () => {
  const query: Record<string, string> = {}
  if (keyword.value) query.keyword = keyword.value
  if (categoryId.value) query.category_id = String(categoryId.value)
  router.replace({ query })
})
</script>

<style scoped>
.book-list-page {
  padding-top: 32px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 4px;
}

.page-header p {
  color: var(--fb-text-secondary);
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  margin-bottom: 24px;
}

.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  min-height: 200px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 32px;
}
</style>
