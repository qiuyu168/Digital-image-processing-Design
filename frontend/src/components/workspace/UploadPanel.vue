<template>
  <section class="panel-card upload-card">
    <div class="panel-title">
      <div class="title-left">
        <span class="title-icon">📤</span>
        <div>
          <h3>上传图片</h3>
        </div>
      </div>
    </div>

    <el-upload
      class="image-uploader"
      action="#"
      :auto-upload="false"
      :show-file-list="false"
      :on-change="(file) => $emit('file-change', file)"
      :disabled="uploadLoading"
      accept=".jpg,.jpeg,.png,.bmp,.webp,.tif,.tiff"
    >
      <div class="upload-box" :class="{ 'has-image': previewDisplayUrl }">
        <template v-if="previewDisplayUrl">
          <div class="image-frame upload-preview-frame">
            <el-image
              class="preview-image"
              :src="previewDisplayUrl"
              fit="contain"
              :preview-src-list="[previewDisplayUrl]"
              :preview-teleported="true"
              :z-index="3000"
              hide-on-click-modal
              @error="$emit('preview-error')"
            >
              <template #error>
                <div class="image-error">
                  <el-icon><Picture /></el-icon>
                  <span>图片预览失败</span>
                </div>
              </template>
            </el-image>
          </div>

          <div class="image-mask">
            <el-icon><UploadFilled /></el-icon>
            <span>点击重新上传</span>
          </div>
        </template>

        <template v-else>
          <el-icon class="upload-icon"><UploadFilled /></el-icon>
          <h4>选择本地图片</h4>
          <p>支持 jpg、jpeg、png、bmp、webp、tif、tiff，大小 10KB - 5MB</p>
        </template>
      </div>
    </el-upload>

    <div v-if="uploadLoading" class="upload-loading">
      <el-icon class="is-loading"><Refresh /></el-icon>
      正在上传图片...
    </div>

    <div v-if="uploadedImage.id" class="image-meta">
      <div>
        <span>文件名</span>
        <strong>{{ uploadedImage.name }}</strong>
      </div>
      <div>
        <span>尺寸</span>
        <strong>{{ uploadedImageSizeText }}</strong>
      </div>
      <div>
        <span>大小</span>
        <strong>{{ formatFileSize(uploadedImage.size) }}</strong>
      </div>
      <div>
        <span>图片路径</span>
        <strong>{{ uploadedImage.id }}</strong>
      </div>
    </div>

    <div v-if="uploadedImage.id" class="upload-actions">
      <el-button plain class="ghost-btn" @click="$emit('clear')">
        <el-icon><Delete /></el-icon>
        移除图片
      </el-button>
    </div>
  </section>
</template>

<script setup>
import { Delete, Picture, Refresh, UploadFilled } from '@element-plus/icons-vue'

defineProps({
  uploadedImage: { type: Object, required: true },
  uploadLoading: { type: Boolean, default: false },
  previewDisplayUrl: { type: String, default: '' },
  uploadedImageSizeText: { type: String, default: '' }
})

defineEmits(['file-change', 'clear', 'preview-error'])

function formatFileSize(size) {
  if (!size) return '0 KB'
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`
  return `${(size / 1024 / 1024).toFixed(2)} MB`
}
</script>

<style lang="scss" scoped>
.panel-card {
  padding: 24px;
  border-radius: var(--radius-lg);
  background: #fff;
  border: 1px solid var(--c-line);
  box-shadow: var(--shadow-1);
}

.panel-title {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
}

.title-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  border-radius: var(--radius-md);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  background: var(--c-cream-2);
  border: 1px solid var(--c-line);
}

.panel-title h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: var(--c-ink);
  letter-spacing: -0.2px;
}

.image-uploader {
  width: 100%;
}

.upload-box {
  position: relative;
  min-height: 280px;
  max-height: 420px;
  border-radius: var(--radius-lg);
  border: 1.5px dashed var(--c-line);
  background: var(--c-cream);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: border-color var(--dur-base) var(--ease-standard),
              background var(--dur-base) var(--ease-standard);
}

.upload-box:hover {
  border-color: rgba(217, 119, 6, 0.35);
  background: #fff;
}

.upload-box.has-image {
  border-style: solid;
  padding: 10px;
}

.image-frame {
  width: 100%;
  border-radius: var(--radius-md);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--c-cream);
  border: 1px solid var(--c-line);
}

.upload-preview-frame {
  min-height: 220px;
  height: clamp(220px, 34vw, 360px);
  max-height: 360px;
}

.preview-image {
  width: 100%;
  height: 100%;
}

:deep(.preview-image .el-image__inner) {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.upload-icon {
  color: var(--c-amber);
  font-size: 42px;
}

.upload-box h4 {
  margin: 0;
  font-size: 15px;
  font-weight: 700;
  color: var(--c-ink);
}

.upload-box p {
  max-width: 360px;
  margin: 0;
  color: var(--c-ink-2);
  font-size: 12px;
  line-height: 1.6;
  text-align: center;
}

.image-mask {
  position: absolute;
  inset: 10px;
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #fff;
  font-weight: 600;
  font-size: 13px;
  background: rgba(43, 36, 25, 0.55);
  opacity: 0;
  transition: opacity var(--dur-base) var(--ease-standard);
}

.image-mask .el-icon {
  font-size: 30px;
}

.upload-box.has-image:hover .image-mask {
  opacity: 1;
}

.image-error {
  width: 100%;
  height: 100%;
  min-height: 180px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: var(--c-ink-2);
  font-size: 13px;
}

.image-error .el-icon {
  color: var(--c-amber);
  font-size: 36px;
}

.upload-loading {
  margin-top: 12px;
  color: var(--c-amber);
  font-size: 13px;
  font-weight: 600;
}

.image-meta {
  margin-top: 16px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.image-meta div {
  min-width: 0;
  padding: 10px 12px;
  border-radius: var(--radius-md);
  background: var(--c-cream);
  border: 1px solid var(--c-line);
}

.image-meta span {
  display: block;
  margin-bottom: 4px;
  color: var(--c-ink-2);
  font-size: 11px;
  letter-spacing: 0.3px;
  text-transform: uppercase;
}

.image-meta strong {
  display: block;
  color: var(--c-ink);
  font-size: 13px;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.upload-actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.ghost-btn {
  color: var(--c-ink);
  border: 1px solid var(--c-line);
  background: #fff;
  border-radius: var(--radius-sm);
  font-weight: 600;
  transition: color var(--dur-fast) var(--ease-standard),
              border-color var(--dur-fast) var(--ease-standard),
              background var(--dur-fast) var(--ease-standard);
}

.ghost-btn:hover {
  color: var(--c-amber);
  border-color: rgba(217, 119, 6, 0.3);
  background: rgba(217, 119, 6, 0.06);
}

@media (max-width: 680px) {
  .panel-card {
    padding: 18px;
  }

  .image-meta {
    grid-template-columns: 1fr;
  }
}
</style>
