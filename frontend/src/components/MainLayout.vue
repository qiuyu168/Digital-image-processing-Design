<!-- 本文件用于集成公共页头、页面主体内容和公共页脚 -->

<script setup>
import HeaderNav from '@/components/HeaderNav.vue'
import AppFooter from '@/components/AppFooter.vue'
</script>

<template>
  <div class="main-layout">
    <!-- 公共页头 -->
    <HeaderNav />
    <!-- 页面主体内容 -->
    <main class="main-content">
      <div class="page-container">
        <RouterView />
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
  background:
    url('@/assets/home_bg.jpg') no-repeat center / cover fixed,
    radial-gradient(circle at 8% 10%, rgba(255, 182, 243, 0.22), transparent 28%),
    radial-gradient(circle at 90% 8%, rgba(142, 216, 255, 0.24), transparent 30%),
    linear-gradient(180deg, #f8faff 0%, #eef4ff 45%, #f9fbff 100%);
}

// 固定并透明导航栏（后续可在 HeaderNav 组件中进一步美化）
:deep(.header-nav) {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.25);   /* 半透明白底，可根据需要调整 */
  backdrop-filter: blur(12px);              /* 背景模糊，增强通透感 */
  -webkit-backdrop-filter: blur(12px);
  transition: background 0.3s ease;
}

.main-content {
  flex: 1;
  position: relative;
  margin-top: 72px;
  padding: 28px 0 40px;
  overflow: hidden;
}

.main-content::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image:
    linear-gradient(rgba(120, 170, 255, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(120, 170, 255, 0.08) 1px, transparent 1px);
  background-size: 36px 36px;
  mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), transparent 80%);
}

.main-content::after {
  content: "✦";
  position: absolute;
  right: 8%;
  top: 40px;
  font-size: 120px;
  color: rgba(255, 160, 230, 0.12);
  pointer-events: none;
}

.page-container {
  position: relative;
  z-index: 1;
  width: 90%;
  margin: 0 auto;
  padding: 0;
}

@media (max-width: 768px) {
  .main-content {
    padding: 20px 0 28px;
  }

  .page-container {
    width: calc(100% - 28px);
  }
}
</style>