<template>
  <div class="not-found-page">
    <div class="not-found-card">
      <div class="error-code">404</div>
      <div class="accent-line"></div>

      <h1>页面迷路了</h1>

      <p>
        你访问的页面不存在，可能是链接输入错误，或者页面已经被移动。
      </p>

      <div class="image-box">
        <div class="image-tip">请返回首页重新开始吧</div>
      </div>

      <div class="action-list">
        <el-button class="main-btn" @click="goHome">
          返回首页
        </el-button>

        <el-button class="ghost-btn" @click="goBack">
          返回上一页
        </el-button>
      </div>
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
.not-found-page {
  min-height: calc(100vh - 200px);
  padding: 60px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--c-ink);
  font-family: var(--font-stack);
}

.not-found-card {
  width: 100%;
  max-width: 480px;
  padding: 48px 32px;
  text-align: center;
}

.error-code {
  font-size: 96px;
  line-height: 1;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--c-ink);
  font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
  animation: nf-fade-up var(--dur-slow) var(--ease-standard) both;
}

.accent-line {
  width: 48px;
  height: 3px;
  margin: 24px auto 28px;
  border-radius: 2px;
  background: var(--c-amber);
  animation: nf-accent-grow var(--dur-base) var(--ease-decel) 80ms both;
  transform-origin: center;
}

h1,
p,
.image-box,
.action-list {
  animation: nf-fade-up var(--dur-base) var(--ease-standard) both;
}

h1 { animation-delay: 140ms; }
p { animation-delay: 200ms; }
.image-box { animation-delay: 260ms; }
.action-list { animation-delay: 320ms; }

@keyframes nf-fade-up {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes nf-accent-grow {
  from { opacity: 0; transform: scaleX(0); }
  to   { opacity: 1; transform: scaleX(1); }
}

.main-btn,
.ghost-btn {
  transition: background var(--dur-fast) var(--ease-standard),
              border-color var(--dur-fast) var(--ease-standard),
              transform var(--dur-fast) var(--ease-standard),
              box-shadow var(--dur-fast) var(--ease-standard);
}

.main-btn:hover,
.ghost-btn:hover {
  transform: translateY(-1px);
}

h1 {
  margin: 0 0 12px;
  font-size: 24px;
  font-weight: 700;
  color: var(--c-ink);
  letter-spacing: -0.3px;
}

p {
  max-width: 380px;
  margin: 0 auto 28px;
  color: var(--c-ink-2);
  font-size: 14px;
  line-height: 1.75;
}

.image-box {
  width: 100%;
  max-width: 320px;
  margin: 0 auto 32px;
  padding: 20px;
  border-radius: var(--radius-md);
  background: var(--c-cream-2);
  border: 1px solid var(--c-line);
}

.image-tip {
  color: var(--c-ink-2);
  font-size: 13px;
  font-weight: 500;
}

.action-list {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.main-btn {
  min-width: 128px;
  height: 42px;
  padding: 0 22px;
  border: none;
  border-radius: var(--radius-md);
  background: var(--c-amber);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  transition: background 0.18s ease;
}

.main-btn:hover,
.main-btn:focus {
  background: var(--c-amber-2);
  color: #fff;
}

.ghost-btn {
  min-width: 128px;
  height: 42px;
  padding: 0 22px;
  border-radius: var(--radius-md);
  background: #fff;
  color: var(--c-ink);
  border: 1px solid var(--c-line);
  font-size: 14px;
  font-weight: 600;
  transition: border-color 0.18s ease, background 0.18s ease;
}

.ghost-btn:hover,
.ghost-btn:focus {
  background: var(--c-cream-2);
  border-color: rgba(43, 36, 25, 0.18);
  color: var(--c-ink);
}

@media (max-width: 640px) {
  .not-found-card {
    padding: 32px 20px;
  }

  .error-code {
    font-size: 72px;
  }

  h1 {
    font-size: 20px;
  }
}
</style>
