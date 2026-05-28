<template>
  <footer class="app-footer glass-card">
    <div class="footer-inner">
      <div class="footer-left">
        <span class="footer-logo">✦</span>
        <span class="footer-title">动漫图像处理系统</span>
      </div>
      <div class="footer-center">
        <span>2025 基于动漫图像识别的交互式数字图像处理系统</span>
        <span class="footer-divider">·</span>
        <span>Vue3 + FastAPI 前后端分离项目</span>
      </div>
      <div class="footer-right">
        <span class="member-tag">总架构/对接: 王韬涵</span>
        <span class="member-tag">前端设计: 聂纪坤</span>
        <span class="member-tag">后端设计: 毛思涵 周恩承 任可 高艳阳 雍晨</span>
      </div>
    </div>
  </footer>
</template>

<style lang="scss" scoped>
.app-footer {
  border-radius: 0;
  border-bottom: none;
  border-left: none;
  border-right: none;
  padding: var(--space-md) var(--space-lg);
}

.footer-inner {
  max-width: 1440px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-sm);
  font-size: 12px;
  color: var(--text-muted);
}

.footer-logo {
  background: linear-gradient(135deg, var(--accent-pink), var(--accent-purple));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 16px;
}

.footer-title {
  font-family: var(--font-display);
  font-weight: 700;
  color: var(--text-secondary);
}

.footer-divider {
  margin: 0 var(--space-xs);
}

.member-tag {
  padding: 2px 8px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.03);
  font-size: 11px;
  transition: background var(--dur-fast);

  &:hover {
    background: rgba(255, 107, 157, 0.1);
  }
}
</style>
