import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      children: [
        { path: '', name: 'Home', component: () => import('@/views/Home.vue') },
        { path: 'books', name: 'BookList', component: () => import('@/views/BookList.vue') },
        { path: 'books/:id', name: 'BookDetail', component: () => import('@/views/BookDetail.vue') },
      ],
    },
    {
      path: '/admin/login',
      name: 'AdminLogin',
      component: () => import('@/views/admin/Login.vue'),
    },
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', redirect: '/admin/dashboard' },
        { path: 'dashboard', name: 'Dashboard', component: () => import('@/views/admin/Dashboard.vue') },
        { path: 'books', name: 'BookManage', component: () => import('@/views/admin/BookManage.vue') },
        { path: 'categories', name: 'CategoryManage', component: () => import('@/views/admin/CategoryManage.vue') },
      ],
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('admin_token')
    if (!token) return '/admin/login'
  }
})

export default router
