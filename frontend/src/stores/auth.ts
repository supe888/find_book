import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('admin_token') || '')
  const isLoggedIn = computed(() => !!token.value)

  async function login(username: string, password: string) {
    const res = await api.adminLogin(username, password)
    token.value = res.access_token
    localStorage.setItem('admin_token', res.access_token)
  }

  function logout() {
    token.value = ''
    localStorage.removeItem('admin_token')
  }

  return { token, isLoggedIn, login, logout }
})
