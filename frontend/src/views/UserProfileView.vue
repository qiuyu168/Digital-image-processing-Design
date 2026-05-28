<template>
  <div class="profile-page">
    <!-- 三个标签按钮 -->
    <div class="tab-bar">
      <el-button
        v-for="tab in tabs"
        :key="tab.key"
        :type="activeTab === tab.key ? 'primary' : 'default'"
        size="large"
        class="tab-button"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </el-button>
    </div>

    <!-- 内容区域 -->
    <div class="tab-content">
      <!-- 基本资料 -->
      <div v-if="activeTab === 'info'" class="content-panel">
        <el-form
          ref="infoFormRef"
          :model="infoForm"
          :rules="infoRules"
          label-width="100px"
          size="large"
          class="info-form"
        >
          <el-form-item label="账号" prop="username">
            <el-input v-model="infoForm.username" disabled />
          </el-form-item>

          <el-form-item label="昵称" prop="nickname">
            <el-input v-model="infoForm.nickname" placeholder="请输入昵称" />
          </el-form-item>

          <el-form-item label="邮箱" prop="email">
            <el-input v-model="infoForm.email" placeholder="请输入邮箱" />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="handleSaveInfo">
              保存修改
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 更换头像 -->
      <div v-else-if="activeTab === 'avatar'" class="content-panel avatar-panel">
        <div class="avatar-preview">
          <el-avatar :size="120" :src="avatarUrl" />
          <p>当前头像预览</p>
        </div>

        <div class="avatar-actions">
          <el-upload
            class="avatar-upload"
            action="#"
            :show-file-list="false"
            :before-upload="handleBeforeAvatarUpload"
            accept="image/*"
          >
            <el-button type="primary">选择新头像</el-button>
          </el-upload>
          <el-button
            v-if="avatarUrl"
            type="danger"
            plain
            @click="removeAvatar"
          >
            移除头像
          </el-button>
        </div>

        <p class="tip">
          支持 jpg / png 格式，大小不超过 2MB。
        </p>
      </div>

      <!-- 设置密码 -->
      <div v-else-if="activeTab === 'password'" class="content-panel">
        <el-form
          ref="passwordFormRef"
          :model="passwordForm"
          :rules="passwordRules"
          label-width="120px"
          size="large"
        >
          <el-form-item label="旧密码" prop="oldPassword">
            <el-input
              v-model="passwordForm.oldPassword"
              type="password"
              show-password
              placeholder="请输入旧密码"
            />
          </el-form-item>

          <el-form-item label="新密码" prop="newPassword">
            <el-input
              v-model="passwordForm.newPassword"
              type="password"
              show-password
              placeholder="请输入新密码"
            />
          </el-form-item>

          <el-form-item label="确认新密码" prop="confirmPassword">
            <el-input
              v-model="passwordForm.confirmPassword"
              type="password"
              show-password
              placeholder="请再次输入新密码"
            />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="handleChangePassword">
              修改密码
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

// ---------- 三个标签页定义 ----------
const tabs = [
  { key: 'info', label: '基本资料' },
  { key: 'avatar', label: '更换头像' },
  { key: 'password', label: '设置密码' }
]

const activeTab = ref('info')

const userStore = useAuthStore()
const router = useRouter()

// ---------- 基本资料 ----------
const infoFormRef = ref(null)
const infoForm = reactive({
  username: userStore.userInfo?.username || '',
  nickname: userStore.userInfo?.nickname || '',
  email: userStore.userInfo?.email || ''
})
const infoRules = {
  nickname: [
    { max: 20, message: '昵称不能超过20个字符', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' },
    { required: true, message: '邮箱不能为空' }
  ]
}

function handleSaveInfo() {
  infoFormRef.value?.validate((valid) => {
    if (valid) {
      ElMessage.success('个人信息已更新')
      userStore.setLoginInfo(userStore.token, {
        ...userStore.userInfo,
        username: infoForm.username,
        nickname: infoForm.nickname,
        email: infoForm.email
      })
    } else {
      ElMessage.error('请检查输入')
    }
  })
}

// ---------- 更换头像 ----------
const avatarUrl = ref('')

function handleBeforeAvatarUpload(file) {
  const isImage = file.type.startsWith('image/')
  if (!isImage) {
    ElMessage.error('只能上传图片文件')
    return false
  }
  const isLt2M = file.size / 1024 / 1024 < 2
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB')
    return false
  }

  const reader = new FileReader()
  reader.onload = (e) => {
    avatarUrl.value = e.target?.result
  }
  reader.readAsDataURL(file)

  ElMessage.success('头像已更新（本地预览）')
  // TODO: 实际上传头像 API
  return false
}

function removeAvatar() {
  avatarUrl.value = ''
  // TODO: 调用删除头像 API
  ElMessage.info('头像已移除')
}

// ---------- 设置密码 ----------
const passwordFormRef = ref(null)
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const checkOldSame = (rule, value, callback) => {
  if (value == passwordForm.value.oldPassword)
    callback(new Error('原密码和新密码不能一致！'))
  else
    callback()
}

const checkNewSame = (rule, value, callback) => {
  if (value != passwordForm.value.newPassword)
    callback(new Error('新密码和确认再次输入的新密码不一致!'))
  else
    callback()
}

const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入密码', trigger: 'blur' },
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    {
      pattern: /^\S{6,15}$/,
      message: '密码长度必须是6-15位的非空字符串',
      trigger: 'blur'
    },
    { validator: checkOldSame, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次确认新密码', trigger: 'blur' },
    {
      pattern: /^\S{6,15}$/,
      message: '密码长度必须是6-15位的非空字符串',
      trigger: 'blur'
    },
    { validator: checkNewSame, trigger: 'blur' }
  ]
}

function handleChangePassword() {
  passwordFormRef.value?.validate((valid) => {
    if (valid) {
      ElMessage.success('密码已修改')
      // 清空表单
      userStore.clearLoginInfo()
      router.push('/login')
    } else {
      ElMessage.error('请检查输入')
    }
  })
}
</script>

<style lang="scss" scoped>
.profile-page {
  font-family: 'M PLUS Rounded 1c', 'Quicksand', sans-serif;
  color: #1a1a1a;
  max-width: 960px;
  margin: 0 auto;
  padding: 0 16px;
}

/* 标签按钮栏 */
.tab-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
  justify-content: center;
}

.tab-button {
  border-radius: 28px;
  font-weight: 600;
  padding: 10px 28px;
  border: none;
  background: rgba(255, 255, 255, 0.8);
  color: #333;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  transition: all 0.2s;
}

.tab-button:hover {
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

.tab-button.el-button--primary {
  background: #ff6b8b;
  color: #fff;
  box-shadow: 0 6px 16px rgba(255, 107, 139, 0.3);
}

/* 内容面板 */
.content-panel {
  width: 100%;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.9);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.04);
}

.info-form {
  :deep(.el-input__wrapper) {
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.6);
    box-shadow: none;
    border: 1px solid rgba(0, 0, 0, 0.06);
  }

  :deep(.el-form-item__label) {
    font-weight: 600;
    color: #1a1a1a;
  }
}

/* 头像区域 */
.avatar-panel {
  text-align: center;
}

.avatar-preview {
  margin-bottom: 24px;

  .el-avatar {
    border: 4px solid rgba(255, 255, 255, 0.8);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
  }

  p {
    margin-top: 12px;
    color: #666;
    font-size: 14px;
  }
}

.avatar-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-bottom: 20px;
}

.tip {
  color: #999;
  font-size: 13px;
  line-height: 1.6;
}

/* 响应式 */
@media (max-width: 680px) {
  .tab-bar {
    flex-wrap: wrap;
    gap: 8px;
  }

  .content-panel {
    padding: 24px;
  }

  .info-form :deep(.el-form-item) {
    display: block;
    margin-bottom: 16px;

    .el-form-item__label {
      text-align: left;
    }
  }
}
</style>