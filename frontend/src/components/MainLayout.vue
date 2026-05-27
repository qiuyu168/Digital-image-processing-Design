<!-- 本文件用于集成公共页头、页面主体内容和公共页脚 -->

<script setup>
import HeaderNav from '@/components/HeaderNav.vue'
import AppFooter from '@/components/AppFooter.vue'
import WarmDust from '@/components/anime/WarmDust.vue'
</script>

<template>
  <div class="main-layout">
    <!-- 全局暖色尘埃(极淡) -->
    <WarmDust />

    <!-- 公共页头 -->
    <HeaderNav />
    <!-- 页面主体内容 -->
    <main class="main-content">
      <div class="page-container">
        <RouterView v-slot="{ Component, route }">
          <Transition name="route-fade" mode="out-in">
            <component :is="Component" :key="route.path" />
          </Transition>
        </RouterView>
      </div>
    </main>
    <!-- 公共页脚 -->
    <AppFooter />
  </div>
</template>

<style lang="scss" scoped>
@import url(../styles/index.scss);

.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: var(--font-stack);
  color: var(--c-ink);
  background:
    radial-gradient(circle at 8% 92%, rgba(217, 119, 6, 0.06), transparent 30%),
    radial-gradient(circle at 92% 8%, rgba(240, 217, 194, 0.18), transparent 32%),
    linear-gradient(180deg, var(--c-cream) 0%, var(--c-cream-2) 100%);
}

:deep(.header-nav) {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  background: rgba(250, 247, 242, 0.72);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--c-line);
  transition: background 0.3s ease;
}

.main-content {
  flex: 1;
  position: relative;
  margin-top: 64px;
  padding: 32px 0 48px;
}

.page-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

@media (max-width: 768px) {
  .main-content {
    padding: 24px 0 32px;
  }

  .page-container {
    padding: 0 16px;
  }
}
</style>
