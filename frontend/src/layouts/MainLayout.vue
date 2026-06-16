<template>
  <div class="main-layout">
    <AppHeader />
    <main class="main-content">
      <router-view />
    </main>
    <footer class="site-footer">
      <div class="page-container">
        <p>自由图书 &copy; 2026 - 免费电子书资源分享平台</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import AppHeader from '@/components/AppHeader.vue'
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding-bottom: 40px;
}

.site-footer {
  background: var(--fb-white);
  border-top: 1px solid #e4e6eb;
  padding: 20px 0;
  text-align: center;
  color: var(--fb-text-secondary);
  font-size: 14px;
}
</style>
