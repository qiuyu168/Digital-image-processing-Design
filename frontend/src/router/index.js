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
                    path: 'library',
                    name: 'Library',
                    component: () => import('@/views/LibraryView.vue'),
                    meta: {
                      title: '图像库'
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
        },
        {
            path: '/:pathMatch(.*)*',
            name: 'NotFound',
            component: () => import('@/views/NotFoundView.vue'),
            meta: {
                title: '页面不存在'
            }
        }
    ]
})

const appTitle = import.meta.env.VITE_APP_TITLE || '数字图像处理系统'

router.afterEach((to) => {
  const pageTitle = to.meta?.title

  document.title = pageTitle ? `${pageTitle} - ${appTitle}` : appTitle
})

export default router
