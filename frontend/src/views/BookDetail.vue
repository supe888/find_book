<template>
  <div v-loading="loading" class="page-container detail-page">
    <template v-if="book">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/books' }">全部图书</el-breadcrumb-item>
        <el-breadcrumb-item>{{ book.title }}</el-breadcrumb-item>
      </el-breadcrumb>

      <div class="detail-card card">
        <div class="detail-main">
          <div class="cover-section">
            <img :src="book.cover_url || defaultCover" :alt="book.title" class="cover" />
          </div>
          <div class="info-section">
            <h1 class="title">{{ book.title }}</h1>
            <p class="author">作者：{{ book.author || '未知' }}</p>

            <div class="tags-row">
              <el-tag type="primary" effect="plain">{{ book.file_format }}</el-tag>
              <el-tag v-if="book.file_size" effect="plain">{{ book.file_size }}</el-tag>
              <el-tag v-if="book.category" type="info" effect="plain">{{ book.category.name }}</el-tag>
              <el-tag v-for="tag in tagList" :key="tag" effect="plain">{{ tag }}</el-tag>
            </div>

            <div class="stats-row">
              <span><el-icon><View /></el-icon> {{ book.view_count }} 浏览</span>
              <span><el-icon><Download /></el-icon> {{ book.download_count }} 下载</span>
            </div>

            <div class="description">
              <h3>内容简介</h3>
              <p>{{ book.description || '暂无简介' }}</p>
            </div>
          </div>
        </div>

        <div class="download-section">
          <h3>
            <el-icon><Link /></el-icon> 网盘下载
          </h3>
          <div v-if="book.download_links?.length" class="download-list">
            <div v-for="link in book.download_links" :key="link.id" class="download-item">
              <div class="platform-info">
                <div class="platform-icon" :class="platformClass(link.platform)">
                  {{ link.platform.charAt(0) }}
                </div>
                <div>
                  <strong>{{ link.platform }}</strong>
                  <p v-if="link.is_primary" class="primary-tag">推荐</p>
                </div>
              </div>
              <el-button type="primary" size="large" @click="handleDownload(link, true)">
                <el-icon><Download /></el-icon> 立即下载
              </el-button>
              <el-button @click="handleDownload(link, false)">
                复制链接
              </el-button>
            </div>
          </div>
          <el-empty v-else description="暂无下载链接" />
        </div>
      </div>
    </template>

    <el-dialog v-model="dialogVisible" title="下载信息" width="480px" align-center>
      <div v-if="currentLink" class="link-dialog">
        <p class="dialog-platform">{{ currentLink.platform }}</p>
        <div class="link-field">
          <label>分享链接</label>
          <div class="copy-row">
            <el-input :model-value="currentLink.link_url" readonly />
            <el-button @click="copyText(currentLink.link_url)">复制</el-button>
          </div>
        </div>
        <div v-if="currentLink.extract_code" class="link-field">
          <label>提取码</label>
          <div class="copy-row">
            <el-input :model-value="currentLink.extract_code" readonly />
            <el-button @click="copyText(currentLink.extract_code)">复制</el-button>
          </div>
        </div>
        <el-button type="primary" style="width: 100%; margin-top: 16px" @click="openLink">
          打开网盘链接
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { api, type Book, type DownloadLink } from '@/api'

const route = useRoute()
const book = ref<Book | null>(null)
const loading = ref(false)
const dialogVisible = ref(false)
const currentLink = ref<DownloadLink | null>(null)

const defaultCover = 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400'

const tagList = computed(() =>
  book.value?.tags ? book.value.tags.split(',').map((t) => t.trim()).filter(Boolean) : []
)

function platformClass(platform: string) {
  if (platform.includes('百度')) return 'baidu'
  if (platform.includes('夸克')) return 'quark'
  if (platform.includes('阿里')) return 'ali'
  if (platform.includes('城通')) return 'ctfile'
  return 'default'
}

async function handleDownload(link: DownloadLink, openDirectly: boolean) {
  if (!book.value) return
  try {
    const res = await api.recordDownload(book.value.id, link.id)
    book.value.download_count += 1
    if (openDirectly) {
      window.open(res.link_url, '_blank')
      if (res.extract_code) {
        ElMessage.success(`已打开下载页，提取码：${res.extract_code}`)
      }
    } else {
      currentLink.value = res
      dialogVisible.value = true
    }
  } catch {
    ElMessage.error('获取下载链接失败')
  }
}

function copyText(text: string) {
  navigator.clipboard.writeText(text)
  ElMessage.success('已复制到剪贴板')
}

function openLink() {
  if (currentLink.value) {
    window.open(currentLink.value.link_url, '_blank')
  }
}

onMounted(async () => {
  loading.value = true
  try {
    book.value = await api.getBook(Number(route.params.id))
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.detail-page {
  padding-top: 24px;
}

.el-breadcrumb {
  margin-bottom: 20px;
}

.detail-card {
  overflow: hidden;
}

.detail-main {
  display: flex;
  gap: 36px;
  padding: 32px;
}

.cover-section {
  flex-shrink: 0;
}

.cover {
  width: 220px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.info-section {
  flex: 1;
}

.title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
  line-height: 1.3;
}

.author {
  color: var(--fb-text-secondary);
  font-size: 16px;
  margin-bottom: 16px;
}

.tags-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.stats-row {
  display: flex;
  gap: 24px;
  color: var(--fb-text-secondary);
  font-size: 14px;
  margin-bottom: 24px;
}

.stats-row span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.description h3 {
  font-size: 16px;
  margin-bottom: 10px;
  color: var(--fb-text);
}

.description p {
  line-height: 1.8;
  color: var(--fb-text-secondary);
}

.download-section {
  border-top: 1px solid #e4e6eb;
  padding: 24px 32px 32px;
  background: var(--fb-blue-light);
}

.download-section h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  margin-bottom: 16px;
  color: #1877f2;
}

.download-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.download-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  padding: 16px 20px;
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  gap: 12px;
}

.download-item .el-button + .el-button {
  margin-left: 0;
}

.platform-info {
  display: flex;
  align-items: center;
  gap: 14px;
}

.platform-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 700;
  font-size: 18px;
}

.platform-icon.baidu { background: #2932e1; }
.platform-icon.quark { background: #ff6a00; }
.platform-icon.ali { background: #ff6a00; }
.platform-icon.ctfile { background: #e74c3c; }
.platform-icon.default { background: #1877f2; }

.primary-tag {
  font-size: 12px;
  color: #1877f2;
  margin-top: 2px;
}

.link-dialog .dialog-platform {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #1877f2;
}

.link-field {
  margin-bottom: 12px;
}

.link-field label {
  display: block;
  font-size: 13px;
  color: var(--fb-text-secondary);
  margin-bottom: 6px;
}

.copy-row {
  display: flex;
  gap: 8px;
}

@media (max-width: 768px) {
  .detail-main {
    flex-direction: column;
    padding: 20px;
  }

  .cover {
    width: 160px;
  }
}
</style>
