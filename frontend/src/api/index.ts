import axios from 'axios'

const http = axios.create({
  baseURL: '/api',
  timeout: 15000,
})

http.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

http.interceptors.response.use(
  (res) => res.data,
  (err) => {
    const msg = err.response?.data?.detail || '请求失败'
    return Promise.reject(new Error(typeof msg === 'string' ? msg : JSON.stringify(msg)))
  }
)

export interface Category {
  id: number
  name: string
  slug: string
  sort_order: number
  book_count?: number
}

export interface DownloadLink {
  id: number
  platform: string
  link_url: string
  extract_code: string
  password: string
  is_primary: boolean
}

export interface DownloadLinkInput {
  platform: string
  link_url: string
  extract_code?: string
  password?: string
  is_primary?: boolean
}

export interface BookInput {
  title: string
  author?: string
  cover_url?: string
  description?: string
  category_id?: number | null
  tags?: string
  file_format?: string
  file_size?: string
  is_published?: boolean
  download_links?: DownloadLinkInput[]
}

export interface Book {
  id: number
  title: string
  author: string
  cover_url: string
  description: string
  category_id: number | null
  tags: string
  file_format: string
  file_size: string
  download_count: number
  view_count: number
  is_published: boolean
  created_at: string
  category?: Category
  download_links?: DownloadLink[]
}

export interface PageResult<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export interface Stats {
  total_books: number
  published_books?: number
  total_downloads: number
  total_categories: number
}

export const api = {
  getCategories: () => http.get<never, Category[]>('/categories'),
  getPublicStats: () => http.get<never, Stats>('/stats'),
  getBooks: (params: { page?: number; page_size?: number; keyword?: string; category_id?: number }) =>
    http.get<never, PageResult<Book>>('/books', { params }),
  getHotBooks: (limit = 8) => http.get<never, Book[]>('/books/hot', { params: { limit } }),
  getBook: (id: number) => http.get<never, Book>(`/books/${id}`),
  recordDownload: (bookId: number, linkId: number) =>
    http.post<never, DownloadLink>(`/books/${bookId}/download`, null, { params: { link_id: linkId } }),

  adminLogin: (username: string, password: string) =>
    http.post<never, { access_token: string }>('/admin/login', { username, password }),
  getStats: () => http.get<never, Stats>('/admin/stats'),
  adminGetCategories: () => http.get<never, Category[]>('/admin/categories'),
  createCategory: (data: Partial<Category>) => http.post<never, Category>('/admin/categories', data),
  updateCategory: (id: number, data: Partial<Category>) =>
    http.put<never, Category>(`/admin/categories/${id}`, data),
  deleteCategory: (id: number) => http.delete(`/admin/categories/${id}`),
  adminGetBooks: (params: { page?: number; page_size?: number; keyword?: string }) =>
    http.get<never, PageResult<Book>>('/admin/books', { params }),
  adminGetBook: (id: number) => http.get<never, Book>(`/admin/books/${id}`),
  createBook: (data: BookInput) => http.post<never, Book>('/admin/books', data),
  updateBook: (id: number, data: BookInput) => http.put<never, Book>(`/admin/books/${id}`, data),
  deleteBook: (id: number) => http.delete(`/admin/books/${id}`),
}

export default http
