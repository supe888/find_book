<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6" v-for="item in statCards" :key="item.label">
        <div class="stat-card card">
          <div class="stat-icon" :style="{ background: item.color }">
            <el-icon :size="28" color="#fff"><component :is="item.icon" /></el-icon>
          </div>
          <div class="stat-info">
            <p class="stat-value">{{ item.value }}</p>
            <p class="stat-label">{{ item.label }}</p>
          </div>
        </div>
      </el-col>
    </el-row>

    <div class="welcome-card card">
      <h2>欢迎使用 自由图书 管理后台</h2>
      <p>您可以在此管理电子书数据、分类和网盘下载链接。</p>
      <div class="quick-actions">
        <el-button type="primary" @click="router.push('/admin/books')">
          <el-icon><Plus /></el-icon> 添加图书
        </el-button>
        <el-button @click="router.push('/admin/categories')">
          <el-icon><Menu /></el-icon> 管理分类
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api, type Stats } from '@/api'

const router = useRouter()
const stats = ref<Stats>({ total_books: 0, published_books: 0, total_downloads: 0, total_categories: 0 })

const statCards = computed(() => [
  { label: '图书总数', value: stats.value.total_books, icon: 'Notebook', color: '#1877F2' },
  { label: '已上架', value: stats.value.published_books, icon: 'CircleCheck', color: '#42B72A' },
  { label: '总下载量', value: stats.value.total_downloads, icon: 'Download', color: '#F5533D' },
  { label: '分类数量', value: stats.value.total_categories, icon: 'FolderOpened', color: '#8B5CF6' },
])

onMounted(async () => {
  stats.value = await api.getStats()
})
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  color: var(--fb-text-secondary);
  font-size: 14px;
}

.welcome-card {
  padding: 32px;
}

.welcome-card h2 {
  font-size: 22px;
  margin-bottom: 8px;
}

.welcome-card p {
  color: var(--fb-text-secondary);
  margin-bottom: 20px;
}

.quick-actions {
  display: flex;
  gap: 12px;
}
</style>
