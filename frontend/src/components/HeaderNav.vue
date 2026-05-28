<template>
  <header class="header-nav glass-card">
    <div class="nav-inner">
      <router-link to="/home" class="logo-area">
        <span class="logo-icon">✦</span>
        <div class="logo-text">
          <span class="logo-title">动漫图像处理系统</span>
          <span class="logo-sub">Anime Image Processing</span>
        </div>
      </router-link>

      <nav class="nav-links">
        <router-link to="/home" class="nav-link" active-class="nav-link--active">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </router-link>
        <router-link to="/workspace" class="nav-link" active-class="nav-link--active">
          <el-icon><MagicStick /></el-icon>
          <span>图像处理</span>
        </router-link>
        <router-link to="/library" class="nav-link" active-class="nav-link--active">
          <el-icon><Picture /></el-icon>
          <span>图像库</span>
        </router-link>
        <router-link to="/profile" class="nav-link" active-class="nav-link--active">
          <el-icon><UserFilled /></el-icon>
          <span>个人中心</span>
        </router-link>
      </nav>

      <div class="user-area">
        <template v-if="authStore.isLogin">
          <div class="user-avatar">{{ (authStore.userInfo?.username || 'U')[0].toUpperCase() }}</div>
          <span class="user-name">{{ authStore.userInfo?.username }}</span>
          <el-icon class="logout-btn" @click="handleLogout"><CloseBold /></el-icon>
        </template>
        <router-link v-else to="/login" class="btn-gradient" style="padding:6px 16px;font-size:13px;">
          登录 / 注册
        </router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { House, MagicStick, Picture, UserFilled, CloseBold } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

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
  right: 0;
  z-index: 100;
  height: 64px;
  border-radius: 0;
  border-top: none;
  border-left: none;
  border-right: none;
}

.nav-inner {
  max-width: 1440px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 var(--space-lg);
  gap: var(--space-xl);
}

.logo-area {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  text-decoration: none;
  flex-shrink: 0;
}

.logo-icon {
  font-size: 28px;
  background: linear-gradient(135deg, var(--accent-pink), var(--accent-purple));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: logoSpin 8s linear infinite;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
}

.logo-sub {
  font-size: 10px;
  color: var(--text-muted);
  line-height: 1.2;
}

.nav-links {
  display: flex;
  gap: var(--space-xs);
  flex: 1;
  justify-content: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 13px;
  font-family: var(--font-body);
  transition: all var(--dur-fast) var(--ease-smooth);
  position: relative;

  &:hover {
    color: var(--text-primary);
    background: rgba(255, 255, 255, 0.04);
  }

  &--active {
    color: var(--accent-pink);
    background: rgba(255, 107, 157, 0.1);

    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 20px;
      height: 3px;
      border-radius: 2px;
      background: var(--accent-pink);
    }
  }
}

.user-area {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  flex-shrink: 0;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent-pink), var(--accent-purple));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  color: #fff;
}

.user-name {
  font-size: 13px;
  color: var(--text-secondary);
}

.logout-btn {
  color: var(--text-muted);
  cursor: pointer;
  font-size: 16px;
  transition: color var(--dur-fast);

  &:hover {
    color: var(--accent-rose);
  }
}

@keyframes logoSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
