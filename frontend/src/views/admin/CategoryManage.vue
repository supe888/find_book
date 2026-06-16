<template>
  <div class="category-manage">
    <div class="toolbar">
      <el-button type="primary" @click="openDialog()">
        <el-icon><Plus /></el-icon> 新增分类
      </el-button>
    </div>

    <el-table :data="categories" v-loading="loading" class="card" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="分类名称" />
      <el-table-column prop="slug" label="标识" />
      <el-table-column prop="sort_order" label="排序" width="100" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button text type="primary" @click="openDialog(row)">编辑</el-button>
          <el-popconfirm title="确定删除该分类？" @confirm="handleDelete(row.id)">
            <template #reference>
              <el-button text type="danger">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="editingId ? '编辑分类' : '新增分类'" width="420px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="名称" required>
          <el-input v-model="form.name" placeholder="分类名称" />
        </el-form-item>
        <el-form-item label="标识" required>
          <el-input v-model="form.slug" placeholder="英文标识，如 computer" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sort_order" :min="0" />
        </el-form-item>
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
import { api, type Category } from '@/api'

const categories = ref<Category[]>([])
const loading = ref(false)
const saving = ref(false)
const dialogVisible = ref(false)
const editingId = ref<number | null>(null)

const form = reactive({ name: '', slug: '', sort_order: 0 })

function openDialog(row?: Category) {
  if (row) {
    editingId.value = row.id
    form.name = row.name
    form.slug = row.slug
    form.sort_order = row.sort_order
  } else {
    editingId.value = null
    form.name = ''
    form.slug = ''
    form.sort_order = 0
  }
  dialogVisible.value = true
}

async function fetchData() {
  loading.value = true
  try {
    categories.value = await api.adminGetCategories()
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  if (!form.name || !form.slug) {
    ElMessage.warning('请填写完整信息')
    return
  }
  saving.value = true
  try {
    if (editingId.value) {
      await api.updateCategory(editingId.value, { ...form })
    } else {
      await api.createCategory({ ...form })
    }
    ElMessage.success('保存成功')
    dialogVisible.value = false
    await fetchData()
  } catch (e: unknown) {
    ElMessage.error(e instanceof Error ? e.message : '保存失败')
  } finally {
    saving.value = false
  }
}

async function handleDelete(id: number) {
  try {
    await api.deleteCategory(id)
    ElMessage.success('删除成功')
    await fetchData()
  } catch (e: unknown) {
    ElMessage.error(e instanceof Error ? e.message : '删除失败')
  }
}

onMounted(fetchData)
</script>

<style scoped>
.toolbar {
  margin-bottom: 16px;
}

.el-table {
  border-radius: 12px;
  overflow: hidden;
}
</style>
