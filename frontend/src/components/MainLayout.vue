<template>
  <div class="main-layout">
    <div class="bg-particles">
      <div
        v-for="p in particles"
        :key="p.id"
        class="floating-particle"
        :style="{
          width: p.size + 'px',
          height: p.size + 'px',
          left: p.x + '%',
          top: p.y + '%',
          background: p.color,
          animation: `float-particle ${p.duration}s ease-in-out infinite`,
          animationDelay: p.delay + 's'
        }"
      />
    </div>
    <HeaderNav />
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="route-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <AppFooter />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import HeaderNav from './HeaderNav.vue'
import AppFooter from './AppFooter.vue'

const colors = ['rgba(255,107,157,0.15)', 'rgba(167,139,250,0.12)', 'rgba(56,189,248,0.1)', 'rgba(52,211,153,0.08)']
const particles = ref(
  Array.from({ length: 16 }, (_, i) => ({
    id: i,
    size: Math.random() * 80 + 20,
    x: Math.random() * 100,
    y: Math.random() * 100,
    color: colors[i % colors.length],
    duration: Math.random() * 20 + 30,
    delay: Math.random() * 10
  }))
)
</script>

<style lang="scss" scoped>
.main-layout {
  min-height: 100vh;
  background: var(--bg-primary);
  position: relative;
  overflow: hidden;
}

.bg-particles {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.main-content {
  position: relative;
  z-index: 1;
  padding-top: 64px;
  min-height: calc(100vh - 64px - 80px);
}

@keyframes float-particle {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(12px, -20px) scale(1.1); }
  50% { transform: translate(-8px, -36px) scale(0.9); }
  75% { transform: translate(-16px, -12px) scale(1.05); }
}
</style>
