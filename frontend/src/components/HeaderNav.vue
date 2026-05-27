<template>
  <header class="header-nav">
    <div class="nav-inner">
      <!-- Logo 区域 -->
      <div class="logo-area" @click="goHome">
        <span class="logo-dot"></span>
        <div class="logo-text">
          <div class="logo-title">动漫图像处理系统</div>
          <div class="logo-subtitle">Anime Image Processing</div>
        </div>
      </div>

      <!-- 中间导航 -->
      <nav class="nav-menu">
        <div
          v-for="item in navItems"
          :key="item.path"
          class="nav-item"
          :class="{ active: isActive(item.path) }"
          @click="goPage(item.path)"
        >
          <el-icon class="nav-icon">
            <component :is="item.icon" />
          </el-icon>
          <span>{{ item.label }}</span>
        </div>
      </nav>

      <!-- 用户区域 -->
      <div class="user-area">
        <!-- 已登录 -->
        <template v-if="authStore.isLogin">
          <div class="user-box" @click="goPage('/profile')">
            <div class="avatar">
              {{ usernameFirstChar }}
            </div>
            <span class="username">
              {{ username }}
            </span>
            <el-icon class="arrow-icon">
              <ArrowRight />
            </el-icon>
          </div>
          <el-icon class="logout-icon" @click.stop="handleLogout">
            <CloseBold />
          </el-icon>
        </template>

        <!-- 未登录 -->
        <template v-else>
          <el-button class="login-register-btn" @click="goPage('/login')">
            登录 / 注册
          </el-button>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  ArrowRight,
  CloseBold,
  House,
  MagicStick,
  Picture,
  UserFilled
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/authStore'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const navItems = [
  { label: '首页', path: '/home', icon: House },
  { label: '图像处理', path: '/workspace', icon: MagicStick },
  { label: '图像库', path: '/library', icon: Picture },
  { label: '用户个人信息', path: '/profile', icon: UserFilled }
]

const username = computed(() => {
  return authStore.userInfo?.username || authStore.userInfo?.name || '用户'
})

const usernameFirstChar = computed(() => {
  return username.value ? username.value.slice(0, 1).toUpperCase() : 'U'
})

function isActive(path) {
  return route.path === path
}

function goHome() {
  router.push('/home')
}

function goPage(path) {
  router.push(path)
}

function handleLogout() {
  authStore.clearLoginInfo()
  router.push('/login')
}
</script>

<style lang="scss" scoped>
.header-nav {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  height: 64px;
  background: rgba(250, 247, 242, 0.72);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--c-line);
}

.nav-inner {
  height: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
}

/* Logo */
.logo-area {
  width: 260px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  user-select: none;
}

.logo-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--c-amber);
  flex-shrink: 0;
}

.logo-title {
  color: var(--c-ink);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.2px;
  line-height: 1.2;
}

.logo-subtitle {
  margin-top: 2px;
  color: var(--c-ink-2);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.6px;
}

/* 导航菜单 */
.nav-menu {
  flex: 1;
  display: flex;
  justify-content: center;
  gap: 4px;
}

.nav-item {
  position: relative;
  height: 64px;
  padding: 0 16px;
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--c-ink-2);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: color var(--dur-fast) var(--ease-standard);

  &::after {
    content: "";
    position: absolute;
    left: 16px;
    right: 16px;
    bottom: 14px;
    height: 2px;
    border-radius: 2px;
    background: var(--c-amber);
    opacity: 0;
    transform: scaleX(0);
    transform-origin: left;
    transition: opacity var(--dur-fast) var(--ease-standard),
                transform var(--dur-base) var(--ease-decel);
  }

  &:hover {
    color: var(--c-ink);
  }

  &.active {
    color: var(--c-ink);
    font-weight: 600;

    &::after {
      opacity: 1;
      transform: scaleX(1);
    }
  }

  .nav-icon {
    font-size: 15px;
  }
}

/* 用户区域 */
.user-area {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 8px;
}

.user-box {
  height: 36px;
  padding: 0 10px 0 4px;
  border-radius: 999px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--c-ink);
  cursor: pointer;
  background: transparent;
  border: 1px solid var(--c-line);
  max-width: 36px;
  overflow: hidden;
  transition: max-width var(--dur-base) var(--ease-standard),
              background var(--dur-fast) var(--ease-standard),
              border-color var(--dur-fast) var(--ease-standard);

  &:hover {
    max-width: 200px;
    background: rgba(217, 119, 6, 0.06);
    border-color: rgba(217, 119, 6, 0.25);
  }
}

.avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--c-amber);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 13px;
  font-weight: 700;
}

.username {
  max-width: 100px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  font-size: 13px;
  font-weight: 600;
}

.arrow-icon {
  font-size: 12px;
  color: var(--c-ink-2);
  transition: transform 0.2s;
}

.user-box:hover .arrow-icon {
  transform: translateX(2px);
  color: var(--c-amber);
}

.logout-icon {
  font-size: 16px;
  color: var(--c-ink-2);
  cursor: pointer;
  padding: 6px;
  border-radius: var(--radius-sm);
  transition: background 0.18s ease, color 0.18s ease;

  &:hover {
    color: var(--c-amber-2);
    background: rgba(217, 119, 6, 0.08);
  }
}

.login-register-btn {
  height: 36px;
  padding: 0 18px;
  border: none;
  border-radius: var(--radius-sm);
  background: var(--c-amber);
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.3px;
  transition: background 0.18s ease;

  &:hover {
    background: var(--c-amber-2);
    color: #fff;
  }
}

@media (max-width: 900px) {
  .nav-inner {
    padding: 0 16px;
  }

  .logo-area {
    width: auto;
  }

  .logo-subtitle {
    display: none;
  }

  .nav-item {
    padding: 0 10px;
    font-size: 13px;
  }

  .user-area {
    width: auto;
  }

  .username {
    display: none;
  }
}
</style>
