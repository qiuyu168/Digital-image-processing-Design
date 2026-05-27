import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/authStore'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
})

http.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
}, Promise.reject)

http.interceptors.response.use(
  (response) => response.data,
  (error) => {
    // 允许跳过全局提示
    if (!error.config?.skipErrorTip) {
      const msg =
        error.response?.data?.message ||
        error.response?.data?.detail ||
        error.message ||
        '请求失败'
      ElMessage.error(msg)
    }
    // TODO: 根据状态码处理 401 等
    return Promise.reject(error)
  }
)

export default http