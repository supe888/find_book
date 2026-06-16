<template>
  <el-container class="admin-layout">
    <el-aside width="240px" class="admin-aside">
      <div class="logo">
        <el-icon :size="28"><Reading /></el-icon>
        <span>自由图书 管理</span>
      </div>
      <el-menu
        :default-active="route.path"
        router
        background-color="#1877F2"
        text-color="#e7f3ff"
        active-text-color="#ffffff"
      >
        <el-menu-item index="/admin/dashboard">
          <el-icon><DataAnalysis /></el-icon>
          <span>数据概览</span>
        </el-menu-item>
        <el-menu-item index="/admin/books">
          <el-icon><Notebook /></el-icon>
          <span>图书管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/categories">
          <el-icon><Menu /></el-icon>
          <span>分类管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="admin-header">
        <span class="header-title">{{ pageTitle }}</span>
        <div class="header-actions">
          <el-button text @click="router.push('/')">
            <el-icon><HomeFilled /></el-icon> 返回前台
          </el-button>
          <el-button type="danger" plain @click="handleLogout">退出登录</el-button>
        </div>
      </el-header>
      <el-main class="admin-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const titles: Record<string, string> = {
  '/admin/dashboard': '数据概览',
  '/admin/books': '图书管理',
  '/admin/categories': '分类管理',
}

const pageTitle = computed(() => titles[route.path] || '管理后台')

function handleLogout() {
  auth.logout()
  router.push('/admin/login')
}
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
}

.admin-aside {
  background: #1877f2;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px;
  color: #fff;
  font-size: 18px;
  font-weight: 700;
}

.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}

.header-title {
  font-size: 18px;
  font-weight: 600;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.admin-main {
  background: var(--fb-blue-bg);
  min-height: calc(100vh - 60px);
}

:deep(.el-menu) {
  border-right: none;
}

:deep(.el-menu-item.is-active) {
  background: rgba(255, 255, 255, 0.15) !important;
  border-radius: 8px;
  margin: 4px 8px;
  width: calc(100% - 16px);
}
</style>
