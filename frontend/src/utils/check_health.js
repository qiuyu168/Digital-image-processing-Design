import http from "@/api/http"

export const chech_health = async () => {
    try {
        const data = await http.get('/api/health')
        if (data.success)
            ElMessage.success(data.message)
        else
            ElMessage.error('服务器异常！')
    } catch (e) {
        ElMessage.error('服务器异常！')
    }
    
}