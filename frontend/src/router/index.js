import { useAuthStore } from '@/stores/authStore'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/home'
        },
        {
            path: '/login',
            name: 'Login',
            component: () => import('@/views/LoginView.vue'),
            meta: {
              title: '登录注册'
            }
        },
        {
            path: '/',
            component: () => import('@/components/MainLayout.vue'),
            children: [
                {
                    path: 'home',
                    name: 'Home',
                    component: () => import('@/views/HomeView.vue'),
                    meta: {
                        title: '首页'
                    }
                },
                {
                    path: 'workspace',
                    name: 'Workspace',
                    component: () => import('@/views/WorkspaceView.vue'),
                    meta: {
                        title: '图像处理'
                    }
                },
                {
                    path: 'profile',
                    name: 'UserProfile',
                    component: () => import('@/views/UserProfileView.vue'),
                    meta: {
                        title: '用户个人信息'
                    }
                }
            ]
        }
    ]
})

// router.beforeEach((to) => {
//     const authStore = useAuthStore()

//     document.title = to.meta.title ? `${to.meta.title} - 数字图像处理系统` : '数字图像处理系统'

//     if (!authStore.isLogin)
//         return '/login'
//     return '/home'
// })

export default router
