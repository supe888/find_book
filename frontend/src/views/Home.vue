<template>
  <div class="home">
    <section class="hero">
      <div class="page-container hero-content">
        <h1>自由图书</h1>
        <p>海量免费电子书，网盘直链下载</p>
        <div class="hero-search">
          <el-input
            v-model="keyword"
            placeholder="搜索书名、作者、标签..."
            size="large"
            @keyup.enter="goSearch"
          >
            <template #append>
              <el-button type="primary" @click="goSearch">
                <el-icon><Search /></el-icon> 搜索
              </el-button>
            </template>
          </el-input>
        </div>
        <div class="hero-stats">
          <div class="stat-item">
            <strong>{{ stats.total_books || '—' }}</strong>
            <span>本图书</span>
          </div>
          <div class="stat-item">
            <strong>{{ stats.total_categories || '—' }}</strong>
            <span>个分类</span>
          </div>
          <div class="stat-item">
            <strong>{{ stats.total_downloads || '—' }}</strong>
            <span>次下载</span>
          </div>
        </div>
      </div>
    </section>

    <section class="page-container section">
      <h2 class="section-title">热门分类</h2>
      <div class="category-grid">
        <router-link
          v-for="cat in categories"
          :key="cat.id"
          :to="`/books?category_id=${cat.id}`"
          class="category-card card"
        >
          <el-icon :size="32" color="#1877F2"><FolderOpened /></el-icon>
          <span class="cat-name">{{ cat.name }}</span>
          <span class="cat-count">{{ cat.book_count }} 本</span>
        </router-link>
      </div>
    </section>

    <section class="page-container section">
      <div class="section-header">
        <h2 class="section-title">热门推荐</h2>
        <router-link to="/books" class="more-link">查看全部 →</router-link>
      </div>
      <div v-loading="loading" class="book-grid">
        <BookCard v-for="book in hotBooks" :key="book.id" :book="book" />
      </div>
    </section>

    <section class="page-container section">
      <div class="section-header">
        <h2 class="section-title">最新上架</h2>
      </div>
      <div v-loading="loadingLatest" class="book-grid">
        <BookCard v-for="book in latestBooks" :key="book.id" :book="book" />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api, type Book, type Category, type Stats } from '@/api'
import BookCard from '@/components/BookCard.vue'

const router = useRouter()
const keyword = ref('')
const categories = ref<Category[]>([])
const hotBooks = ref<Book[]>([])
const latestBooks = ref<Book[]>([])
const stats = ref<Partial<Stats>>({})
const loading = ref(false)
const loadingLatest = ref(false)

function goSearch() {
  router.push({ path: '/books', query: keyword.value ? { keyword: keyword.value } : {} })
}

onMounted(async () => {
  loading.value = true
  loadingLatest.value = true
  try {
    const [cats, hot, latest, publicStats] = await Promise.all([
      api.getCategories(),
      api.getHotBooks(8),
      api.getBooks({ page: 1, page_size: 8 }),
      api.getPublicStats(),
    ])
    categories.value = cats
    hotBooks.value = hot
    latestBooks.value = latest.items
    stats.value = publicStats
  } finally {
    loading.value = false
    loadingLatest.value = false
  }
})
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, #1877f2 0%, #0a5dc2 50%, #004db3 100%);
  padding: 60px 0 70px;
  color: #fff;
  margin-bottom: 40px;
}

.hero-content {
  text-align: center;
}

.hero h1 {
  font-size: 42px;
  font-weight: 800;
  margin-bottom: 12px;
  letter-spacing: -1px;
}

.hero p {
  font-size: 18px;
  opacity: 0.9;
  margin-bottom: 32px;
}

.hero-search {
  max-width: 560px;
  margin: 0 auto 36px;
}

.hero-search :deep(.el-input-group__append) {
  background: #fff;
  border: none;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 48px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-item strong {
  font-size: 28px;
  font-weight: 700;
}

.stat-item span {
  font-size: 14px;
  opacity: 0.8;
}

.section {
  margin-bottom: 48px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.section-header .section-title {
  margin-bottom: 0;
}

.more-link {
  color: #1877f2;
  font-weight: 500;
  font-size: 15px;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 16px;
}

.category-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 24px 16px;
  font-weight: 600;
  color: var(--fb-text);
  cursor: pointer;
}

.cat-name {
  font-size: 15px;
}

.cat-count {
  font-size: 12px;
  color: var(--fb-text-secondary);
  font-weight: 400;
}

.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  min-height: 100px;
}
</style>
