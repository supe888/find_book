<template>
  <header class="app-header">
    <div class="page-container header-inner">
      <router-link to="/" class="logo">
        <div class="logo-icon">
          <el-icon :size="24"><Reading /></el-icon>
        </div>
        <span class="logo-text">自由图书</span>
      </router-link>

      <div class="search-box">
        <el-input
          v-model="keyword"
          placeholder="搜索书名、作者..."
          size="large"
          clearable
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>

      <nav class="nav-links">
        <router-link to="/" class="nav-item" :class="{ active: route.path === '/' }">首页</router-link>
        <router-link to="/books" class="nav-item" :class="{ active: route.path.startsWith('/books') }">全部图书</router-link>
        <router-link to="/admin/login" class="nav-item admin-link">
          <el-icon><Setting /></el-icon> 管理
        </router-link>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const keyword = ref('')

function handleSearch() {
  router.push({ path: '/books', query: keyword.value ? { keyword: keyword.value } : {} })
}
</script>

<style scoped>
.app-header {
  background: #1877f2;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(24, 119, 242, 0.3);
}

.header-inner {
  display: flex;
  align-items: center;
  gap: 24px;
  height: 64px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #fff;
  flex-shrink: 0;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-text {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.search-box {
  flex: 1;
  max-width: 480px;
}

.search-box :deep(.el-input__wrapper) {
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: none;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.nav-item {
  color: rgba(255, 255, 255, 0.85);
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-item:hover,
.nav-item.active {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
}

.admin-link {
  background: rgba(255, 255, 255, 0.1);
}
</style>
