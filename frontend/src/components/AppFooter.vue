<template>
  <footer class="app-footer">
    <div class="footer-inner">
      <div class="footer-top">
        <div class="footer-brand">
          <div class="brand-row">
            <span class="brand-dot"></span>
            <span class="brand-name">动漫图像处理系统</span>
          </div>
        </div>
        <div class="footer-info">
          <p>© {{ year }} 基于动漫图像识别的交互式数字图像处理系统</p>
          <p>数字图像处理课程设计 · Vue3 + FastAPI 前后端分离项目</p>
        </div>
      </div>

      <div class="footer-team">
        <div class="team-group">
          <h4 class="team-category">总架构设计/前后端对接</h4>
          <div class="team-members">
            <span class="member-tag">王韬涵</span>
          </div>
        </div>
        <div class="team-group">
          <h4 class="team-category">前端设计/前后端对接</h4>
          <div class="team-members">
            <span class="member-tag">聂纪坤</span>
          </div>
        </div>
        <div class="team-group">
          <h4 class="team-category">后端设计(不分先后)</h4>
          <div class="team-members">
            <span class="member-tag">毛思涵</span>
            <span class="member-tag">周恩承</span>
            <span class="member-tag">任可</span>
            <span class="member-tag">高艳阳</span>
            <span class="member-tag">雍晨</span>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
const year = new Date().getFullYear()
</script>

<style lang="scss" scoped>
.app-footer {
  position: relative;
  background: var(--c-cream-2);
  border-top: 1px solid var(--c-line);
  color: var(--c-ink-2);
}

.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.footer-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
}

.footer-brand {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.brand-row {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--c-ink);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.2px;
}

.brand-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--c-amber);
}

.footer-info {
  p {
    margin: 4px 0;
    font-size: 13px;
    line-height: 1.7;
    color: var(--c-ink-2);

    &:first-child {
      color: var(--c-ink);
      font-weight: 600;
    }
  }
}

.footer-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--c-line);
}

.footer-team {
  display: flex;
  flex-wrap: wrap;
  gap: 24px 32px;
  align-content: center;
}

.team-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 140px;
}

.team-category {
  margin: 0;
  font-size: 11px;
  font-weight: 600;
  color: var(--c-amber);
  letter-spacing: 1px;
  text-transform: uppercase;
}

.team-members {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.member-tag {
  padding: 3px 10px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
  color: var(--c-ink);
  background: #fff;
  border: 1px solid var(--c-line);
  transition: background var(--dur-fast) var(--ease-standard),
              border-color var(--dur-fast) var(--ease-standard);

  &:hover {
    background: var(--c-cream-2);
    border-color: rgba(217, 119, 6, 0.18);
  }
}

@media (max-width: 900px) {
  .footer-inner {
    gap: 20px;
  }

  .footer-top {
    flex-direction: column;
    gap: 16px;
  }
}
</style>
