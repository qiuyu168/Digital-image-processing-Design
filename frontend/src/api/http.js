import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/authStore'

const http = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: 10000
})

http.interceptors.request.use(
    (config) => {
        const authStore = useAuthStore()
        
        if (authStore.token) {
            config.headers.Authorization = `Bearer ${authStore.token}`
        }

        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

http.interceptors.response.use(
    (response) => {
        return response.data
    },
    (error) => {
        const message =
            error.response?.data?.message ||
            error.response?.data?.detail ||
            error.message ||
            '请求失败'

        ElMessage.error(message)

        return Promise.reject(error)
    }
)

export default http