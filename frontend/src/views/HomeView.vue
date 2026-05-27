<template>
  <div class="home-page">
    <div class="home-layout">
      <!-- 主内容区 -->
      <div class="home-main">
        <HeroSection />
        <FlowSection />
        <AlgorithmModuleGrid
          :modules="algorithmModules"
          @select-module="onSelectModule"
        />
        <FeatureSection />
      </div>

      <!-- 右侧锚点目录侧栏 -->
      <aside class="home-toc">
        <div class="toc-inner">
          <div class="toc-label">目录</div>
          <a
            v-for="anchor in tocList"
            :key="anchor.id"
            :href="`#${anchor.id}`"
            class="toc-item"
            :class="{ active: activeAnchor === anchor.id }"
            @click.prevent="scrollTo(anchor.id)"
          >
            {{ anchor.label }}
          </a>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import HeroSection from '@/components/home/HeroSection.vue'
import FlowSection from '@/components/home/FlowSection.vue'
import AlgorithmModuleGrid from '@/components/home/AlgorithmModuleGrid.vue'
import FeatureSection from '@/components/home/FeatureSection.vue'

import { chech_health } from '@/utils/check_health'
import { onMounted, onBeforeUnmount, ref } from 'vue'
import { useRouter } from 'vue-router'

onMounted(() => {
  chech_health()
  setupScrollSpy()
})

onBeforeUnmount(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('scroll', onScroll)
  }
})

const router = useRouter()
const activeAnchor = ref('hero')

const tocList = [
  { id: 'hero', label: '欢迎' },
  { id: 'flow', label: '功能流程' },
  { id: 'modules', label: '算法模块' },
  { id: 'features', label: '项目特色' }
]

const algorithmModules = [
  {
    icon: '🌗',
    title: '灰度图像类',
    desc: '用于完成灰度化、二值化、直方图均衡化和形态学处理等基础操作。',
    tags: ['灰度化', '二值化', '形态学']
  },
  {
    icon: '🎨',
    title: '彩色图像类',
    desc: '用于颜色空间转换、饱和度调整、动漫色彩增强和主色调提取。',
    tags: ['HSV', '饱和度', '主色调']
  },
  {
    icon: '📐',
    title: '几何变换类',
    desc: '用于完成图像缩放、旋转和翻转等基本空间变换。',
    tags: ['缩放', '旋转', '翻转']
  },
  {
    icon: '🫧',
    title: '空域滤波类',
    desc: '通过均值滤波、高斯滤波、中值滤波等方法实现图像平滑与降噪。',
    tags: ['均值滤波', '高斯滤波', '中值滤波']
  },
  {
    icon: '🌌',
    title: '频域分析类',
    desc: '通过傅里叶变换、频谱中心化和幅度谱显示观察图像频域特征。',
    tags: ['傅里叶', '频谱', '幅度谱']
  },
  {
    icon: '⚡',
    title: '频域滤波类',
    desc: '通过低通、高通、理想滤波和高斯滤波实现频域增强与平滑。',
    tags: ['低通', '高通', '高斯频域']
  }
]

function scrollTo(id) {
  const el = document.getElementById(id)
  if (!el) return
  const top = el.getBoundingClientRect().top + window.scrollY - 80
  window.scrollTo({ top, behavior: 'smooth' })
  activeAnchor.value = id
}

function onScroll() {
  const offset = 120
  let current = tocList[0].id
  for (const a of tocList) {
    const el = document.getElementById(a.id)
    if (!el) continue
    if (el.getBoundingClientRect().top - offset <= 0) {
      current = a.id
    }
  }
  activeAnchor.value = current
}

function setupScrollSpy() {
  if (typeof window === 'undefined') return
  window.addEventListener('scroll', onScroll, { passive: true })
  onScroll()
}

function onSelectModule(index) {
  // Handle module selection event from AlgorithmModuleGrid
  console.log('Selected module:', index)
}
</script>

<style lang="scss" scoped>
@import url(@/styles/index.scss);

.home-page {
  color: var(--c-ink);
  font-family: var(--font-stack);
}

.home-layout {
  display: grid;
  grid-template-columns: 1fr 200px;
  gap: 48px;
  align-items: flex-start;
}

.home-main {
  min-width: 0;
}

/* =============== TOC =============== */
.home-toc {
  position: sticky;
  top: 96px;
  align-self: flex-start;
}

.toc-inner {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 16px 0;
  border-left: 1px solid var(--c-line);
}

.toc-label {
  padding: 0 14px 8px;
  font-size: 11px;
  font-weight: 700;
  color: var(--c-amber);
  letter-spacing: 1.5px;
  text-transform: uppercase;
}

.toc-item {
  position: relative;
  padding: 6px 14px;
  font-size: 13px;
  color: var(--c-ink-2);
  text-decoration: none;
  transition: color var(--dur-fast) var(--ease-standard);
  cursor: pointer;

  &::before {
    content: '';
    position: absolute;
    left: -1px;
    top: 50%;
    transform: translateY(-50%);
    width: 2px;
    height: 0;
    background: var(--c-amber);
    transition: height var(--dur-base) var(--ease-standard);
  }

  &:hover {
    color: var(--c-ink);
  }

  &.active {
    color: var(--c-amber);
    font-weight: 600;

    &::before {
      height: 18px;
    }
  }
}

/* =============== Responsive =============== */
@media (max-width: 1100px) {
  .home-layout {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .home-toc {
    display: none;
  }
}
</style>
