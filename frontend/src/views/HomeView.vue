<template>
  <div class="home-page">
    <!-- 一、轮播欢迎区 -->
    <section class="hero-section">
      <el-carousel
        height="460px"
        indicator-position="outside"
        arrow="always"
        class="hero-carousel"
      >
        <el-carousel-item
          v-for="item in carouselList"
          :key="item.title"
        >
          <div class="hero-slide" :class="item.className">
            <div class="hero-mask"></div>

            <div class="hero-content">
              <div class="hero-tag">
                {{ item.tag }}
              </div>

              <h1>{{ item.title }}</h1>

              <p>{{ item.desc }}</p>

              <div class="hero-actions">
                <el-button
                  type="primary"
                  size="large"
                  class="primary-action"
                  @click="goWorkspace"
                >
                  开始处理图像
                </el-button>

                <el-button
                  size="large"
                  class="ghost-action"
                  @click="goProfile"
                >
                  查看个人信息
                </el-button>
              </div>
            </div>

            <div class="hero-panel">
              <div class="anime-window">
                <div class="window-top">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>

                <div class="window-body">
                  <div
                    v-for="step in item.panelSteps"
                    :key="step"
                    class="window-step"
                  >
                    {{ step }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </section>

    <!-- 二、功能流程区 -->
    <section class="section-block">
      <div class="section-title">
        <span class="title-icon">🌸</span>
        <h2>功能流程</h2>
        <p>简单几步，完成动漫图像的处理与预览</p>
      </div>

      <div class="flow-list">
        <div
          v-for="(item, index) in flowList"
          :key="item.title"
          class="flow-card"
        >
          <div class="flow-index">
            {{ index + 1 }}
          </div>

          <div class="flow-icon">
            {{ item.icon }}
          </div>

          <h3>{{ item.title }}</h3>
          <p>{{ item.desc }}</p>

          <div
            v-if="index !== flowList.length - 1"
            class="flow-arrow"
          >
            →
          </div>
        </div>
      </div>
    </section>

    <!-- 三、算法模块区 -->
    <section class="section-block">
      <div class="section-title">
        <span class="title-icon">🌸</span>
        <h2>算法模块</h2>
        <p>{{ dynamicModules.length > 0 ? dynamicModules.length + '大图像处理方向，覆盖数字图像处理核心算法' : '六大图像处理方向，覆盖数字图像处理核心算法' }}</p>
      </div>

      <div v-if="modulesLoading" class="module-grid">
        <div v-for="n in 6" :key="n" class="module-card skeleton-card">
          <el-skeleton :rows="3" animated />
        </div>
      </div>

      <div v-else class="module-grid">
        <div
          v-for="item in displayModules"
          :key="item.title"
          class="module-card"
          @click="goWorkspace"
        >
          <div class="module-icon">
            {{ item.icon }}
          </div>

          <div class="module-content">
            <h3>{{ item.title }}</h3>
            <p>{{ item.desc }}</p>

            <div class="module-tags">
              <span
                v-for="tag in item.tags"
                :key="tag"
              >
                {{ tag }}
              </span>
            </div>
          </div>

          <div class="module-more">
            进入处理
          </div>
        </div>
      </div>
    </section>

    <!-- 四、项目特色区 -->
    <section class="section-block feature-section">
      <div class="section-title">
        <span class="title-icon">🌸</span>
        <h2>项目特色</h2>
        <p>精心设计，兼顾功能体验与视觉表现</p>
      </div>

      <div class="feature-grid">
        <div
          v-for="item in featureList"
          :key="item.title"
          class="feature-card"
        >
          <div class="feature-icon">
            {{ item.icon }}
          </div>

          <h3>{{ item.title }}</h3>
          <p>{{ item.desc }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { chech_health } from '@/utils/check_health'
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAlgorithmService } from '@/api/algorithms'

const router = useRouter()

const dynamicModules = ref([])
const modulesLoading = ref(false)

async function loadModules() {
  modulesLoading.value = true
  try {
    const data = await getAlgorithmService()
    const rawModules = Array.isArray(data?.modules) ? data.modules : []
    dynamicModules.value = rawModules.map(function(m) {
      return {
        icon: '\u{1F338}',
        title: m.display_name || m.module,
        desc: '共 ' + (Array.isArray(m.algorithms) ? m.algorithms.length : 0) + ' 个算法',
        tags: (Array.isArray(m.algorithms) ? m.algorithms.slice(0, 3) : []).map(function(a) { return a.display_name || a.name })
      }
    })
  } catch {
    dynamicModules.value = []
  } finally {
    modulesLoading.value = false
  }
}

const displayModules = computed(function() {
  return dynamicModules.value.length > 0 ? dynamicModules.value : algorithmModules
})

onMounted(function() {
  chech_health()
  loadModules()
})

const carouselList = [
  {
    tag: 'Anime Image Processing',
    title: '基于动漫图像识别的交互式数字图像处理系统',
    desc: '支持动漫人物、头像、插画、场景截图等图片的上传、算法处理、结果展示与分析。',
    className: 'slide-one',
    panelSteps: ['上传图片', '选择算法', '参数调节', '查看结果']
  },
  {
    tag: 'Digital Image Processing',
    title: '覆盖多类数字图像处理算法',
    desc: '集成灰度、彩色、几何、空域、频域等经典模块，满足多种处理需求。',
    className: 'slide-two',
    panelSteps: ['灰度处理', '空域滤波', '频域分析', '边缘增强']
  },
  {
    tag: 'Visual Experience',
    title: '直观的交互与可视化反馈',
    desc: '每一步操作都配有即时预览与对比，帮助你直观理解图像处理效果。',
    className: 'slide-three',
    panelSteps: ['原图预览', '处理过程', '结果对比', '细节查看']
  }
]

const flowList = [
  {
    icon: '📤',
    title: '上传图片',
    desc: '选择本地动漫图片、头像或插画素材。'
  },
  {
    icon: '🪄',
    title: '选择算法',
    desc: '从灰度、彩色、几何、空域、频域等模块中选择算法。'
  },
  {
    icon: '🎚️',
    title: '调整参数',
    desc: '设置阈值、滤波核、旋转角度等参数。'
  },
  {
    icon: '🖼️',
    title: '查看结果',
    desc: '展示处理前后对比、分步过程与指标分析。'
  }
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

// 项目特色：去掉“报告展示友好”，改为“交互直观”
const featureList = [
  {
    icon: '🧩',
    title: '前后端分离',
    desc: 'Vue3 负责页面交互与结果展示，后端 FastAPI 负责图像处理算法和接口服务。'
  },
  {
    icon: '📦',
    title: '算法模块化',
    desc: '每类算法独立管理，便于小组成员分工开发和后续功能扩展。'
  },
  {
    icon: '🔍',
    title: '处理结果对比',
    desc: '支持原图、结果图和中间步骤图展示，便于观察算法处理效果。'
  },
  {
    icon: '🎯',
    title: '交互直观',
    desc: '界面简洁，操作流畅，每一步都有清晰的视觉反馈与引导。'
  }
]

function goWorkspace() {
  router.push('/workspace')
}

function goProfile() {
  router.push('/profile')
}
</script>

<style lang="scss" scoped>

.home-page {
  color: #1a1a1a;
  font-family: 'M PLUS Rounded 1c', 'Quicksand', 'Noto Sans JP', sans-serif;
}

/* =========================
   一、欢迎区（轮播）
========================= */
.hero-section {
  margin-bottom: 48px;
}

.hero-carousel {
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(8px);
}

.hero-slide {
  position: relative;
  height: 100%;
  padding: 0 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(255, 255, 255, 0.85);
  border-radius: 24px;
  backdrop-filter: blur(8px);
}

.hero-mask {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.9);
  z-index: 1;
}

.slide-one {
  background: rgba(255, 255, 255, 0.9);
}

.slide-two {
  background: rgba(255, 255, 255, 0.9);
}

.slide-three {
  background: rgba(255, 255, 255, 0.9);
}

.hero-slide::before {
  content: "";
  position: absolute;
  width: 450px;
  height: 450px;
  right: -120px;
  top: -120px;
  border-radius: 50%;
  background: rgba(255, 182, 193, 0.15);
  z-index: 2;
}

.hero-slide::after {
  content: "🌸";
  position: absolute;
  right: 10%;
  top: 40px;
  color: rgba(255, 150, 180, 0.35);
  font-size: 70px;
  z-index: 2;
  animation: floatSakura 6s ease-in-out infinite;
}

@keyframes floatSakura {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-10px) rotate(8deg); }
}

.hero-content {
  position: relative;
  z-index: 3;
  width: 60%;
}

.hero-tag {
  display: inline-flex;
  padding: 5px 16px;
  margin-bottom: 20px;
  border-radius: 999px;
  font-size: 13px;
  letter-spacing: 1px;
  color: #ff5277;
  background: rgba(255, 82, 119, 0.1);
  border: 1px solid rgba(255, 82, 119, 0.25);
}

.hero-content h1 {
  max-width: 700px;
  margin: 0 0 18px;
  font-size: 38px;
  line-height: 1.3;
  font-weight: 800;
  color: #1a1a1a;
}

.hero-content p {
  max-width: 640px;
  margin: 0 0 28px;
  color: #333;
  font-size: 16px;
  line-height: 1.8;
}

.hero-actions {
  display: flex;
  gap: 16px;
}

.primary-action {
  border: none;
  background: #ff6b8b;
  color: #fff;
  font-weight: 700;
  box-shadow: 0 6px 16px rgba(255, 107, 139, 0.35);
  border-radius: 24px;
  padding: 12px 28px;
  transition: all 0.2s;
}

.primary-action:hover {
  background: #ff5277;
  box-shadow: 0 8px 20px rgba(255, 82, 119, 0.45);
  color: #fff;
}

.ghost-action {
  color: #1a1a1a;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 24px;
  padding: 12px 28px;
  font-weight: 600;
  backdrop-filter: blur(4px);
}

.ghost-action:hover {
  background: rgba(255, 255, 255, 0.95);
  border-color: rgba(0, 0, 0, 0.2);
  color: #000;
}

/* 右侧模拟面板 */
.hero-panel {
  position: relative;
  z-index: 3;
  width: 30%;
  display: flex;
  justify-content: flex-end;
}

.anime-window {
  width: 280px;
  padding: 16px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
}

.window-top {
  display: flex;
  gap: 6px;
  margin-bottom: 16px;
}

.window-top span {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #ffb7c5;
}

.window-top span:nth-child(2) {
  background: #ffe0a8;
}

.window-top span:nth-child(3) {
  background: #a8e6cf;
}

.window-body {
  display: grid;
  gap: 10px;
}

.window-step {
  height: 48px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  color: #1a1a1a;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.95);
}

/* =========================
   公共区块
========================= */
.section-block {
  margin-bottom: 56px;
}

.section-title {
  text-align: center;
  margin-bottom: 32px;
}

.title-icon {
  display: inline-flex;
  width: 44px;
  height: 44px;
  margin-bottom: 12px;
  border-radius: 14px;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: #ff5277;
  background: rgba(255, 255, 255, 0.9);
}

.section-title h2 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
}

.section-title p {
  margin: 8px 0 0;
  color: #333;
  font-size: 15px;
}

/* =========================
   二、功能流程区
========================= */
.flow-list {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.flow-card {
  position: relative;
  min-height: 200px;
  padding: 24px 20px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.95);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  transition: all 0.3s;
}

.flow-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.1);
}

.flow-index {
  position: absolute;
  right: 18px;
  top: 14px;
  font-size: 36px;
  font-weight: 800;
  color: gray;
}

.flow-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 16px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  background: rgba(255, 107, 139, 0.1);
}

.flow-card h3 {
  margin: 0 0 10px;
  font-size: 18px;
  color: #1a1a1a;
  font-weight: 700;
}

.flow-card p {
  margin: 0;
  line-height: 1.7;
  color: #333;
  font-size: 14px;
}

.flow-arrow {
  position: absolute;
  right: -16px;
  top: 50%;
  transform: translateY(-50%);
  color: #aaa;
  font-size: 24px;
  z-index: 2;
}

/* =========================
   三、算法模块区
========================= */
.module-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.module-card {
  position: relative;
  min-height: 240px;
  padding: 24px 22px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.95);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  cursor: pointer;
  transition: all 0.3s;
}

.module-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.12);
}

.module-icon {
  width: 52px;
  height: 52px;
  margin-bottom: 16px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  background: rgba(255, 107, 139, 0.1);
}

.module-content h3 {
  margin: 0 0 10px;
  font-size: 20px;
  color: #1a1a1a;
  font-weight: 700;
}

.module-content p {
  min-height: 70px;
  margin: 0 0 16px;
  color: #333;
  line-height: 1.7;
  font-size: 14px;
}

.module-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.module-tags span {
  padding: 4px 10px;
  border-radius: 999px;
  color: #333;
  font-size: 12px;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.module-more {
  position: absolute;
  right: 20px;
  bottom: 20px;
  color: #ff6b8b;
  font-size: 13px;
  font-weight: 700;
}

/* =========================
   四、项目特色区
========================= */
.feature-section {
  margin-bottom: 10px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.feature-card {
  min-height: 210px;
  padding: 24px 20px;
  border-radius: 20px;
  text-align: center;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.95);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  width: 52px;
  height: 52px;
  margin: 0 auto 16px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  background: rgba(255, 107, 139, 0.1);
}

.feature-card h3 {
  margin: 0 0 10px;
  color: #1a1a1a;
  font-size: 18px;
  font-weight: 700;
}

.feature-card p {
  margin: 0;
  line-height: 1.7;
  color: #333;
  font-size: 14px;
}

/* =========================
   轮播指示器
========================= */
:deep(.el-carousel__indicators--outside) {
  margin-top: 12px;
}

:deep(.el-carousel__button) {
  width: 20px;
  height: 4px;
  border-radius: 999px;
  background-color: #ddd;
  opacity: 0.8;
}

:deep(.el-carousel__button.is-active) {
  background-color: #ff6b8b;
  opacity: 1;
}

/* =========================
   响应式
========================= */
@media (max-width: 1100px) {
  .hero-slide {
    padding: 0 40px;
  }

  .hero-content h1 {
    font-size: 32px;
  }

  .hero-panel {
    display: none;
  }

  .hero-content {
    width: 100%;
  }

  .flow-list,
  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .module-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .flow-arrow {
    display: none;
  }
}

@media (max-width: 680px) {
  .hero-slide {
    padding: 0 24px;
  }

  .hero-content h1 {
    font-size: 26px;
  }

  .hero-content p {
    font-size: 14px;
  }

  .hero-actions {
    flex-direction: column;
  }

  .flow-list,
  .module-grid,
  .feature-grid {
    grid-template-columns: 1fr;
  }
}
</style>