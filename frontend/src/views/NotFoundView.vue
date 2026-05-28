<template>
    <div class="not-found-page">
      <div class="not-found-card">
        <div class="decor decor-one">🌸</div>
        <div class="decor decor-two">✨</div>
  
        <div class="error-code">404</div>
  
        <h1>页面迷路了</h1>
  
        <p>
          你访问的页面不存在，可能是链接输入错误，或者页面已经被移动。
        </p>
  
        <div class="image-box">
          <div class="image-tip">请返回首页重新开始吧</div>
        </div>
  
        <div class="action-list">
          <el-button class="main-btn" type="primary" @click="goHome">
            返回首页
          </el-button>
  
          <el-button class="ghost-btn" plain @click="goBack">
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
    min-height: calc(100vh - 160px);
    padding: 60px 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #1a1a1a;
    font-family: 'M PLUS Rounded 1c', 'Quicksand', 'Noto Sans JP', sans-serif;
  }
  
  .not-found-card {
    position: relative;
    width: min(760px, 100%);
    padding: 56px 44px;
    border-radius: 28px;
    text-align: center;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.88);
    border: 1px solid rgba(255, 255, 255, 0.95);
    box-shadow: 0 18px 46px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(12px);
  }
  
  .not-found-card::before {
    content: "";
    position: absolute;
    width: 360px;
    height: 360px;
    right: -120px;
    top: -140px;
    border-radius: 50%;
    background: rgba(255, 182, 193, 0.22);
  }
  
  .not-found-card::after {
    content: "";
    position: absolute;
    width: 300px;
    height: 300px;
    left: -110px;
    bottom: -130px;
    border-radius: 50%;
    background: rgba(173, 216, 255, 0.2);
  }
  
  .decor {
    position: absolute;
    z-index: 1;
    font-size: 46px;
    opacity: 0.7;
    animation: floatDecor 5s ease-in-out infinite;
  }
  
  .decor-one {
    left: 46px;
    top: 38px;
  }
  
  .decor-two {
    right: 56px;
    bottom: 42px;
    animation-delay: 1.2s;
  }
  
  @keyframes floatDecor {
    0%,
    100% {
      transform: translateY(0) rotate(0deg);
    }
  
    50% {
      transform: translateY(-10px) rotate(8deg);
    }
  }
  
  .error-code {
    position: relative;
    z-index: 2;
    font-size: 112px;
    line-height: 1;
    font-weight: 900;
    letter-spacing: 6px;
    color: #ff6b8b;
    text-shadow: 0 8px 18px rgba(255, 107, 139, 0.24);
  }
  
  h1 {
    position: relative;
    z-index: 2;
    margin: 18px 0 12px;
    font-size: 32px;
    font-weight: 800;
  }
  
  p {
    position: relative;
    z-index: 2;
    max-width: 520px;
    margin: 0 auto;
    color: #555;
    font-size: 15px;
    line-height: 1.8;
  }
  
  .image-box {
    position: relative;
    z-index: 2;
    width: min(360px, 100%);
    margin: 32px auto 28px;
    padding: 24px;
    border-radius: 22px;
    background:
      radial-gradient(circle at 20% 15%, rgba(255, 182, 193, 0.28), transparent 36%),
      rgba(255, 255, 255, 0.72);
    border: 1px solid rgba(255, 107, 139, 0.14);
  }
  
  .anime-face {
    font-size: 34px;
    font-weight: 800;
    color: #ff5277;
  }
  
  .image-tip {
    margin-top: 10px;
    color: #666;
    font-size: 14px;
  }
  
  .action-list {
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: center;
    gap: 14px;
    flex-wrap: wrap;
  }
  
  .main-btn {
    min-width: 128px;
    height: 42px;
    border: none;
    border-radius: 999px;
    font-weight: 800;
    background: #ff6b8b;
    box-shadow: 0 6px 16px rgba(255, 107, 139, 0.35);
  }
  
  .main-btn:hover,
  .main-btn:focus {
    background: #ff5277;
  }
  
  .ghost-btn {
    min-width: 128px;
    height: 42px;
    border-radius: 999px;
    color: #ff5277;
    border-color: rgba(255, 82, 119, 0.3);
    background: rgba(255, 255, 255, 0.72);
  }
  
  .ghost-btn:hover,
  .ghost-btn:focus {
    color: #fff;
    border-color: #ff6b8b;
    background: #ff6b8b;
  }
  
  @media (max-width: 640px) {
    .not-found-card {
      padding: 44px 24px;
    }
  
    .error-code {
      font-size: 82px;
    }
  
    h1 {
      font-size: 26px;
    }
  }
  </style>