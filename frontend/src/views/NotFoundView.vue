<template>
  <div class="notfound-page">
    <div class="nf-glow nf-glow--pink"></div>
    <div class="nf-glow nf-glow--purple"></div>

    <h1 class="nf-code gradient-text">404</h1>
    <p class="nf-message">页面飞走了 ✦</p>
    <p class="nf-sub">你访问的页面不存在或已被移除</p>

    <div class="nf-actions">
      <router-link to="/home" class="btn-gradient">返回首页</router-link>
      <button class="btn-glass" @click="$router.go(-1)">返回上一页</button>
    </div>
  </div>
</template>
  
  <script setup>
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  function goHome() {
    router.push('/home')
  }
  
  function goBack() {
    router.back()
  }
  </script>
  
  <style lang="scss" scoped>
.notfound-page {
  min-height: calc(100vh - 64px - 80px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.nf-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.1;
  pointer-events: none;
  &--pink { width: 300px; height: 300px; background: var(--accent-pink); top: 10%; left: 20%; }
  &--purple { width: 250px; height: 250px; background: var(--accent-purple); bottom: 10%; right: 20%; }
}

.nf-code {
  font-family: var(--font-display);
  font-size: 120px;
  font-weight: 800;
  animation: nfBreathe 3s ease-in-out infinite;
  position: relative;
  z-index: 1;
}

.nf-message { font-family: var(--font-display); font-size: 22px; color: var(--text-primary); margin: 0 0 var(--space-sm); position: relative; z-index: 1; }
.nf-sub { font-size: 14px; color: var(--text-muted); margin: 0 0 var(--space-xl); position: relative; z-index: 1; }

.nf-actions { display: flex; gap: var(--space-md); position: relative; z-index: 1; }

@keyframes nfBreathe {
  0%, 100% { opacity: 1; filter: drop-shadow(0 0 20px rgba(255,107,157,0.3)); }
  50% { opacity: 0.85; filter: drop-shadow(0 0 40px rgba(167,139,250,0.4)); }
}
</style>