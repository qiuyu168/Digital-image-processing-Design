<template>
  <header class="header-nav">
    <div class="nav-inner">
      <!-- Logo 区域 -->
      <div class="logo-area" @click="goHome">
        <div class="logo-icon">
          <span>✦</span>
        </div>
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
  UserFilled
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/authStore'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const navItems = [
  {
    label: '首页',
    path: '/home',
    icon: House
  },
  {
    label: '图像处理',
    path: '/workspace',
    icon: MagicStick
  },
  {
    label: '用户个人信息',
    path: '/profile',
    icon: UserFilled
  }
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
  if (typeof authStore.logout === 'function') {
    authStore.logout()
  } else if (typeof authStore.clearLoginInfo === 'function') {
    authStore.clearLoginInfo()
  }
  router.push('/login')
}
</script>

<style lang="scss" scoped>
// ========== 变量定义 ==========
$bg-start: rgba(120, 180, 240, 0.55);
$bg-mid: rgba(180, 220, 255, 0.6);
$bg-end: rgba(200, 235, 255, 0.55);
$text-dark: #0b1e33;
$text-mid: #1a3350;
$text-light: #2c4b6e;
$glow-blue: rgba(79, 172, 254, 0.4);
$glow-cyan: rgba(0, 242, 254, 0.3);
$border-light: rgba(79, 172, 254, 0.3);

.header-nav {
  position: fixed;                // 改为固定定位
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  height: 72px;
  background: rgba(255, 255, 255, 0.25);   // 半透明白底（后续可按需调整）
  backdrop-filter: blur(12px);             // 背景模糊
  -webkit-backdrop-filter: blur(12px);
  // 其余属性（border-bottom, box-shadow 等）可保留，但建议降低阴影透明度
  border-bottom: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);

  // 水波波纹1
  &::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255, 255, 255, 0.4);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    animation: ripple1 4s ease-out infinite;
  }

  // 水波波纹2（延迟启动，形成叠加）
  &::after {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255, 255, 255, 0.25);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    animation: ripple2 4s ease-out 1.5s infinite;
  }
}

@keyframes ripple1 {
  0% {
    width: 0;
    height: 0;
    opacity: 0.7;
  }
  100% {
    width: 500px;
    height: 500px;
    opacity: 0;
  }
}

@keyframes ripple2 {
  0% {
    width: 0;
    height: 0;
    opacity: 0.5;
  }
  100% {
    width: 400px;
    height: 400px;
    opacity: 0;
  }
}

.nav-inner {
  height: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 32px;
  display: flex;
  align-items: center;
  position: relative;
  z-index: 1;
}

/* Logo */
.logo-area {
  width: 300px;
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.logo-icon {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  margin-right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #7ec8f8, #b0e0ff);
  box-shadow:
    0 0 16px rgba(79, 172, 254, 0.5),
    0 0 32px rgba(0, 242, 254, 0.3),
    inset 0 0 8px rgba(255, 255, 255, 0.6);
  animation: iconGlow 2s ease-in-out infinite alternate;

  span {
    color: #fff;
    font-size: 24px;
    font-weight: 700;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.9);
    animation: spinStar 4s linear infinite;
  }
}

@keyframes iconGlow {
  from {
    box-shadow: 0 0 16px rgba(79, 172, 254, 0.5), 0 0 32px rgba(0, 242, 254, 0.3), inset 0 0 8px rgba(255,255,255,0.6);
  }
  to {
    box-shadow: 0 0 24px rgba(79, 172, 254, 0.7), 0 0 48px rgba(0, 242, 254, 0.5), inset 0 0 12px rgba(255,255,255,0.8);
  }
}

@keyframes spinStar {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.logo-title {
  color: $text-dark;
  font-size: 19px;
  font-weight: 700;
  letter-spacing: 1px;
  text-shadow: none;
}

.logo-subtitle {
  margin-top: 3px;
  color: $text-mid;
  font-size: 12px;
  font-weight: 500;
}

/* 导航菜单 */
.nav-menu {
  flex: 1;
  display: flex;
  justify-content: center;
  gap: 14px;
}

.nav-item {
  height: 42px;
  padding: 0 18px;
  border-radius: 999px;
  display: flex;
  align-items: center;
  gap: 7px;
  color: $text-mid;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid transparent;

  &:hover {
    color: $text-dark;
    background: rgba(255, 255, 255, 0.25);
    border-color: $border-light;
    box-shadow: 0 0 10px rgba(79, 172, 254, 0.2);
    transform: translateY(-2px);
  }

  &.active {
    color: $text-dark;
    background: rgba(255, 255, 255, 0.3);
    border-color: rgba(79, 172, 254, 0.5);
    box-shadow: 0 0 12px rgba(79, 172, 254, 0.3);
  }

  .nav-icon {
    font-size: 17px;
    filter: drop-shadow(0 0 4px rgba(79, 172, 254, 0.4));
  }
}

/* 用户区域 */
.user-area {
  width: 260px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
}

.user-box {
  height: 44px;
  padding: 0 14px 0 6px;
  border-radius: 999px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: $text-dark;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid $border-light;
  box-shadow: 0 0 12px rgba(79, 172, 254, 0.1);
  transition: all 0.3s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.35);
    border-color: rgba(79, 172, 254, 0.6);
    box-shadow: 0 0 18px rgba(79, 172, 254, 0.3);
    transform: translateY(-2px);
  }
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #7ec8f8, #b0e0ff);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  box-shadow: 0 0 12px rgba(79, 172, 254, 0.6);
  text-shadow: 0 0 6px rgba(255, 255, 255, 0.8);
}

.username {
  max-width: 100px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  font-size: 14px;
  font-weight: 600;
}

.arrow-icon {
  font-size: 14px;
  color: $text-mid;
  transition: transform 0.3s;
}

.user-box:hover .arrow-icon {
  transform: translateX(3px);
  color: $text-dark;
}

.logout-icon {
  font-size: 20px;
  color: $text-mid;
  cursor: pointer;
  transition: all 0.3s;
  padding: 6px;
  border-radius: 50%;

  &:hover {
    color: #0b1e33;
    background: rgba(255, 255, 255, 0.3);
    transform: scale(1.1);
  }
}

.login-register-btn {
  height: 42px;
  padding: 0 28px;
  border: none;
  border-radius: 999px;
  background: linear-gradient(135deg, #7ec8f8, #b0e0ff);
  color: #0b1e33;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 1px;
  box-shadow:
    0 0 16px rgba(79, 172, 254, 0.4),
    0 0 30px rgba(0, 242, 254, 0.2);
  transition: all 0.3s ease;

  &:hover {
    background: linear-gradient(135deg, #a0d4fc, #c8eaff);
    box-shadow:
      0 0 20px rgba(79, 172, 254, 0.6),
      0 0 40px rgba(0, 242, 254, 0.3);
    transform: translateY(-2px);
  }

  &:active {
    transform: translateY(0);
  }
}

/* 小屏幕适配 */
@media (max-width: 900px) {
  .nav-inner {
    padding: 0 18px;
  }

  .logo-area {
    width: 230px;
  }

  .logo-subtitle {
    display: none;
  }

  .nav-item {
    padding: 0 12px;
  }

  .user-area {
    width: auto;
    gap: 8px;
  }

  .username {
    display: none;
  }
}
</style>