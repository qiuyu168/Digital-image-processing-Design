import { checkHealthService } from "@/api/health"

export const chech_health = async () => {
    try {
        const data = await checkHealthService()
        if (data.success)
            ElMessage.success(data.message)
        else
            ElMessage.error('服务器异常！')
    } catch (e) {
        ElMessage.error('服务器异常！')
    }
    
}