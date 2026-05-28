<template>
  <footer class="app-footer">
    <div class="footer-inner">
      <!-- Logo -->
      <div class="footer-logo">
        <span class="star">✦</span>
        <span>动漫图像处理系统</span>
      </div>

      <!-- 版权信息 -->
      <div class="footer-info">
        <p>© {{ year }} 基于动漫图像识别的交互式数字图像处理系统</p>
        <p>数字图像处理课程设计 · Vue3 + FastAPI 前后端分离项目</p>
      </div>

      <!-- 参与人员 -->
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
// ========== 变量定义 ==========
$bg-start: rgba(120, 180, 240, 0.55);
$bg-mid: rgba(180, 220, 255, 0.6);
$bg-end: rgba(200, 235, 255, 0.55);
$text-dark: #0b1e33;
$text-mid: #1a3350;
$glow-blue: rgba(79, 172, 254, 0.4);
$border-light: rgba(79, 172, 254, 0.3);

.app-footer {
  position: relative;
  background:
    linear-gradient(135deg, $bg-start, $bg-mid, $bg-end),
    radial-gradient(circle at 20% 30%, rgba(79, 172, 254, 0.12), transparent 40%),
    radial-gradient(circle at 80% 50%, rgba(0, 242, 254, 0.08), transparent 40%);
  border-top: 1px solid rgba(255, 255, 255, 0.3);
  color: $text-mid;
  overflow: hidden;

  // 顶部发光线
  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 12%;
    right: 12%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.7), transparent);
    z-index: 1;
  }

  // 水波效果
  &::after {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255, 255, 255, 0.25);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    animation: footerRipple 5s ease-out infinite;
  }
}

@keyframes footerRipple {
  0% {
    width: 0;
    height: 0;
    opacity: 0.6;
  }
  100% {
    width: 450px;
    height: 450px;
    opacity: 0;
  }
}

.footer-inner {
  position: relative;
  z-index: 2;
  max-width: 1280px;
  min-height: 130px;
  margin: 0 auto;
  padding: 24px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 28px;
  flex-wrap: wrap;
}

.footer-logo {
  width: 260px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: $text-dark;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 1px;
}

.star {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #7ec8f8, #b0e0ff);
  box-shadow: 0 0 12px rgba(79, 172, 254, 0.5), 0 0 24px rgba(0, 242, 254, 0.2);
  color: #fff;
  font-size: 18px;
  animation: spinStar 4s linear infinite;
}

@keyframes spinStar {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.footer-info {
  flex: 1;
  text-align: center;
  min-width: 250px;

  p {
    margin: 6px 0;
    font-size: 14px;
    line-height: 1.7;
    color: $text-mid;

    &:first-child {
      color: $text-dark;
      font-weight: 600;
      text-shadow: none;
    }
  }
}

.footer-team {
  width: 380px;
  display: flex;
  justify-content: flex-end;
  gap: 20px;
  flex-wrap: wrap;
}

.team-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.team-category {
  margin: 0;
  font-size: 13px;
  font-weight: 600;
  color: $text-dark;
  text-transform: uppercase;
  letter-spacing: 1px;
  text-shadow: none;
}

.team-members {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 6px;
}

.member-tag {
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 12px;
  color: $text-dark;
  background: rgba(255, 255, 255, 0.3);
  border: 1px solid $border-light;
  box-shadow: 0 0 6px rgba(79, 172, 254, 0.1);
  transition: all 0.3s ease;
  cursor: default;

  &:hover {
    background: rgba(79, 172, 254, 0.2);
    border-color: rgba(79, 172, 254, 0.5);
    box-shadow: 0 0 10px rgba(79, 172, 254, 0.3);
    transform: translateY(-1px);
  }
}

/* 响应式 */
@media (max-width: 900px) {
  .footer-inner {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }

  .footer-logo,
  .footer-team {
    width: 100%;
    justify-content: center;
  }

  .footer-team {
    justify-content: center;
  }

  .footer-info {
    min-width: unset;
  }
}
</style>