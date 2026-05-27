<template>
  <div class="avatar-layout">
    <div class="avatar-preview">
      <el-avatar :size="96" :src="avatarUrl" />
      <p>当前头像预览</p>
    </div>

    <div class="avatar-right">
      <div class="avatar-actions">
        <el-upload
          class="avatar-upload"
          action="#"
          :show-file-list="false"
          :before-upload="handleBeforeUpload"
          accept="image/*"
        >
          <el-button class="primary-btn">选择新头像</el-button>
        </el-upload>
        <el-button
          v-if="avatarUrl"
          class="ghost-btn"
          @click="$emit('remove')"
        >
          移除头像
        </el-button>
      </div>

      <p class="tip">
        支持 jpg / png 格式，大小不超过 2MB。
      </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  avatarUrl: { type: String, default: '' }
})

const emit = defineEmits(['upload', 'remove'])

function handleBeforeUpload(file) {
  emit('upload', file)
  return false
}
</script>

<style scoped>
.avatar-layout {
  display: grid;
  grid-template-columns: 96px 1fr;
  gap: 28px;
  align-items: start;
}

.avatar-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;

  :deep(.el-avatar) {
    background: var(--c-cream-2);
    border: 1px solid var(--c-line);
    box-shadow: var(--shadow-1);
  }

  p {
    color: var(--c-ink-2);
    font-size: 13px;
    white-space: nowrap;
    margin: 0;
  }
}

.avatar-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.tip {
  color: var(--c-ink-2);
  font-size: 12px;
  line-height: 1.6;
  opacity: 0.8;
  margin: 0;
}

.primary-btn {
  height: 40px;
  padding: 0 22px;
  border: none;
  border-radius: var(--radius-md);
  background: var(--c-amber);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.3px;
  transition: background var(--dur-fast) var(--ease-standard);

  &:hover, &:focus {
    background: var(--c-amber-2);
    color: #fff;
  }
}

.ghost-btn {
  height: 40px;
  padding: 0 18px;
  border-radius: var(--radius-md);
  background: #fff;
  color: var(--c-ink);
  border: 1px solid var(--c-line);
  font-size: 14px;
  font-weight: 600;
  transition: border-color var(--dur-fast) var(--ease-standard), background var(--dur-fast) var(--ease-standard);

  &:hover, &:focus {
    background: var(--c-cream-2);
    border-color: rgba(43, 36, 25, 0.18);
    color: var(--c-ink);
  }
}

@media (max-width: 600px) {
  .avatar-layout {
    grid-template-columns: 1fr;
    justify-items: center;
    text-align: center;
  }

  .avatar-actions {
    justify-content: center;
  }
}
</style>
