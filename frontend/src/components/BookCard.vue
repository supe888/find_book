<template>
  <router-link :to="`/books/${book.id}`" class="book-card card">
    <div class="cover-wrap">
      <img :src="book.cover_url || defaultCover" :alt="book.title" class="cover" />
      <span class="format-tag">{{ book.file_format }}</span>
    </div>
    <div class="info">
      <h3 class="title">{{ book.title }}</h3>
      <p class="author">{{ book.author || '未知作者' }}</p>
      <div class="meta">
        <span v-if="book.category" class="category">{{ book.category.name }}</span>
        <span class="downloads">
          <el-icon><Download /></el-icon> {{ book.download_count }}
        </span>
      </div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import type { Book } from '@/api'

defineProps<{ book: Book }>()

const defaultCover = 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400'
</script>

<style scoped>
.book-card {
  display: block;
  overflow: hidden;
  cursor: pointer;
}

.cover-wrap {
  position: relative;
  aspect-ratio: 3/4;
  overflow: hidden;
  background: var(--fb-blue-light);
}

.cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.book-card:hover .cover {
  transform: scale(1.05);
}

.format-tag {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #1877f2;
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 6px;
}

.info {
  padding: 14px 16px 16px;
}

.title {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 6px;
}

.author {
  font-size: 13px;
  color: var(--fb-text-secondary);
  margin-bottom: 10px;
}

.meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
}

.category {
  background: var(--fb-blue-light);
  color: #1877f2;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.downloads {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--fb-text-secondary);
}
</style>
