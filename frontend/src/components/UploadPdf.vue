<template>
  <div class="upload-container">
    <el-upload
      class="upload-dragger"
      action="/api/rag/upload"
      :show-file-list="false"
      :before-upload="beforeUpload"
      :on-success="onSuccess"
      :on-error="onError"
      drag
      accept=".pdf"
    >
      <el-icon class="upload-icon" size="48"><Upload /></el-icon>
      <div class="upload-text">
        <span class="text-primary">点击或拖拽PDF文件到此处上传</span>
        <span class="text-secondary">支持 .pdf 格式文件</span>
      </div>
    </el-upload>
    
    <div v-if="uploading" class="upload-progress">
      <el-progress :percentage="progress" />
      <span class="progress-text">正在上传并处理...</span>
    </div>
    
    <div v-if="success" class="upload-success">
      <el-icon color="#67C23A" size="24"><Checked /></el-icon>
      <span>{{ successMessage }}</span>
    </div>
    
    <div v-if="error" class="upload-error">
      <el-icon color="#F56C6C" size="24"><Warning /></el-icon>
      <span>{{ error }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Upload, Checked, Warning } from '@element-plus/icons-vue'

const emit = defineEmits(['upload-success', 'upload-error'])

const uploading = ref(false)
const progress = ref(0)
const success = ref(false)
const successMessage = ref('')
const error = ref('')

const beforeUpload = (file) => {
  const isPdf = file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')
  if (!isPdf) {
    error.value = '请上传PDF格式文件'
    setTimeout(() => { error.value = '' }, 3000)
    return false
  }
  
  const isLt20M = file.size / 1024 / 1024 < 20
  if (!isLt20M) {
    error.value = '文件大小不能超过20MB'
    setTimeout(() => { error.value = '' }, 3000)
    return false
  }
  
  uploading.value = true
  success.value = false
  error.value = ''
  progress.value = 0
  
  return true
}

const onSuccess = (response) => {
  uploading.value = false
  progress.value = 100
  success.value = true
  successMessage.value = response.message || '上传成功'
  emit('upload-success', response)
  
  setTimeout(() => {
    success.value = false
    successMessage.value = ''
  }, 3000)
}

const onError = (err) => {
  uploading.value = false
  error.value = err.message || '上传失败，请重试'
  emit('upload-error', err)
  
  setTimeout(() => { error.value = '' }, 3000)
}
</script>

<style scoped>
.upload-container {
  width: 100%;
}

.upload-dragger {
  border: 2px dashed #D9D9D9;
  border-radius: 12px;
  background: #FAFAFA;
  transition: all 0.3s ease;
}

.upload-dragger:hover {
  border-color: #409EFF;
  background: #F0F5FF;
}

.upload-dragger :deep(.el-upload__text) {
  color: #909399;
}

.upload-icon {
  color: #409EFF;
  margin-bottom: 12px;
}

.upload-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.text-primary {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.text-secondary {
  font-size: 12px;
  color: #909399;
}

.upload-progress {
  margin-top: 16px;
}

.progress-text {
  display: block;
  text-align: center;
  font-size: 13px;
  color: #409EFF;
  margin-top: 8px;
}

.upload-success {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 16px;
  padding: 12px;
  background: #E8F5E9;
  color: #67C23A;
  border-radius: 8px;
  font-size: 14px;
}

.upload-error {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 16px;
  padding: 12px;
  background: #FEF0F0;
  color: #F56C6C;
  border-radius: 8px;
  font-size: 14px;
}
</style>