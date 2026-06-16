<template>
  <div class="book-manage">
    <div class="toolbar">
      <el-input
        v-model="keyword"
        placeholder="搜索图书..."
        clearable
        style="width: 240px"
        @clear="fetchBooks"
        @keyup.enter="fetchBooks"
      />
      <el-button type="primary" @click="fetchBooks">搜索</el-button>
      <el-button type="primary" @click="openDialog()">
        <el-icon><Plus /></el-icon> 新增图书
      </el-button>
    </div>

    <el-table :data="books" v-loading="loading" class="card" stripe>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column label="封面" width="80">
        <template #default="{ row }">
          <img :src="row.cover_url" class="table-cover" />
        </template>
      </el-table-column>
      <el-table-column prop="title" label="书名" min-width="180" show-overflow-tooltip />
      <el-table-column prop="author" label="作者" width="140" show-overflow-tooltip />
      <el-table-column label="分类" width="100">
        <template #default="{ row }">{{ row.category?.name || '-' }}</template>
      </el-table-column>
      <el-table-column prop="file_format" label="格式" width="80" />
      <el-table-column prop="download_count" label="下载" width="80" />
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.is_published ? 'success' : 'info'" size="small">
            {{ row.is_published ? '上架' : '下架' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <el-button text type="primary" @click="openDialog(row)">编辑</el-button>
          <el-popconfirm title="确定删除该图书？" @confirm="handleDelete(row.id)">
            <template #reference>
              <el-button text type="danger">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination
        v-model:current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        background
        @current-change="fetchBooks"
      />
    </div>

    <el-dialog
      v-model="dialogVisible"
      :title="editingId ? '编辑图书' : '新增图书'"
      width="680px"
      top="5vh"
      destroy-on-close
    >
      <el-form :model="form" label-width="90px">
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="书名" required>
              <el-input v-model="form.title" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="作者">
              <el-input v-model="form.author" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="封面URL">
          <el-input v-model="form.cover_url" placeholder="图片链接" />
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="分类">
              <el-select v-model="form.category_id" placeholder="选择分类" clearable style="width: 100%">
                <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="格式">
              <el-select v-model="form.file_format" style="width: 100%">
                <el-option label="PDF" value="PDF" />
                <el-option label="EPUB" value="EPUB" />
                <el-option label="MOBI" value="MOBI" />
                <el-option label="AZW3" value="AZW3" />
                <el-option label="TXT" value="TXT" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="大小">
              <el-input v-model="form.file_size" placeholder="如 10MB" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="标签">
          <el-input v-model="form.tags" placeholder="逗号分隔，如 编程,经典" />
        </el-form-item>
        <el-form-item label="上架">
          <el-switch v-model="form.is_published" />
        </el-form-item>

        <el-divider content-position="left">网盘下载链接</el-divider>
        <div v-for="(link, index) in form.download_links" :key="index" class="link-form-row">
          <el-select v-model="link.platform" placeholder="平台" style="width: 130px">
            <el-option label="百度网盘" value="百度网盘" />
            <el-option label="夸克网盘" value="夸克网盘" />
            <el-option label="阿里云盘" value="阿里云盘" />
            <el-option label="123云盘" value="123云盘" />
            <el-option label="蓝奏云" value="蓝奏云" />
          </el-select>
          <el-input v-model="link.link_url" placeholder="分享链接" style="flex: 1" />
          <el-input v-model="link.extract_code" placeholder="提取码" style="width: 100px" />
          <el-checkbox v-model="link.is_primary">推荐</el-checkbox>
          <el-button text type="danger" @click="form.download_links.splice(index, 1)">
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
        <el-button text type="primary" @click="addLink">
          <el-icon><Plus /></el-icon> 添加链接
        </el-button>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { api, type Book, type Category, type DownloadLink } from '@/api'

interface LinkForm {
  platform: string
  link_url: string
  extract_code: string
  password: string
  is_primary: boolean
}

const books = ref<Book[]>([])
const categories = ref<Category[]>([])
const loading = ref(false)
const saving = ref(false)
const dialogVisible = ref(false)
const editingId = ref<number | null>(null)
const keyword = ref('')
const page = ref(1)
const pageSize = 10
const total = ref(0)

const defaultForm = () => ({
  title: '',
  author: '',
  cover_url: '',
  description: '',
  category_id: undefined as number | undefined,
  tags: '',
  file_format: 'PDF',
  file_size: '',
  is_published: true,
  download_links: [] as LinkForm[],
})

const form = reactive(defaultForm())

function addLink() {
  form.download_links.push({ platform: '百度网盘', link_url: '', extract_code: '', password: '', is_primary: false })
}

async function openDialog(row?: Book) {
  if (row) {
    editingId.value = row.id
    const detail = await api.adminGetBook(row.id)
    Object.assign(form, {
      title: detail.title,
      author: detail.author,
      cover_url: detail.cover_url,
      description: detail.description,
      category_id: detail.category_id ?? undefined,
      tags: detail.tags,
      file_format: detail.file_format,
      file_size: detail.file_size,
      is_published: detail.is_published,
      download_links: (detail.download_links || []).map((l: DownloadLink) => ({
        platform: l.platform,
        link_url: l.link_url,
        extract_code: l.extract_code,
        password: l.password,
        is_primary: l.is_primary,
      })),
    })
  } else {
    editingId.value = null
    Object.assign(form, defaultForm())
  }
  dialogVisible.value = true
}

async function fetchBooks() {
  loading.value = true
  try {
    const res = await api.adminGetBooks({ page: page.value, page_size: pageSize, keyword: keyword.value || undefined })
    books.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  if (!form.title) {
    ElMessage.warning('请填写书名')
    return
  }
  saving.value = true
  try {
    const payload = { ...form }
    if (editingId.value) {
      await api.updateBook(editingId.value, payload)
    } else {
      await api.createBook(payload)
    }
    ElMessage.success('保存成功')
    dialogVisible.value = false
    await fetchBooks()
  } catch (e: unknown) {
    ElMessage.error(e instanceof Error ? e.message : '保存失败')
  } finally {
    saving.value = false
  }
}

async function handleDelete(id: number) {
  try {
    await api.deleteBook(id)
    ElMessage.success('删除成功')
    await fetchBooks()
  } catch (e: unknown) {
    ElMessage.error(e instanceof Error ? e.message : '删除失败')
  }
}

onMounted(async () => {
  categories.value = await api.adminGetCategories()
  await fetchBooks()
})
</script>

<style scoped>
.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.table-cover {
  width: 40px;
  height: 54px;
  object-fit: cover;
  border-radius: 4px;
}

.pagination {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.link-form-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.el-table {
  border-radius: 12px;
  overflow: hidden;
}
</style>
