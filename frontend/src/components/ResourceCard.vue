<template>
  <el-card class="resource-card" hover>
    <div class="card-header">
      <div class="resource-icon" :style="{ background: iconBg }">
        <component :is="iconComponent" size="24" />
      </div>
      <div class="resource-info">
        <h3 class="resource-title">{{ resource.title }}</h3>
        <span class="resource-type">{{ typeLabel }}</span>
      </div>
    </div>
    <div class="card-body">
      <p class="resource-desc">{{ resource.description }}</p>
    </div>
    <div class="card-footer">
      <span class="create-time">创建于 {{ formatTime(resource.created_at) }}</span>
      <div class="actions">
        <el-button size="small" text @click="$emit('view', resource)">
          <el-icon><View /></el-icon>
        </el-button>
        <el-button size="small" text @click="$emit('regenerate', resource)">
          <el-icon><Refresh /></el-icon>
        </el-button>
        <el-button size="small" text @click="$emit('delete', resource)">
          <el-icon><Delete /></el-icon>
        </el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'
import { Document, Notebook, VideoPlay, DataAnalysis, Picture, View, Refresh, Delete } from '@element-plus/icons-vue'

const props = defineProps({
  resource: {
    type: Object,
    required: true
  }
})

defineEmits(['view', 'regenerate', 'delete'])

const typeMap = {
  document: { label: '文档', icon: Document, color: '#409EFF' },
  mindmap: { label: '思维导图', icon: Notebook, color: '#67C23A' },
  questions: { label: '题库', icon: Notebook, color: '#E6A23C' },
  video: { label: '视频', icon: VideoPlay, color: '#F56C6C' },
  code: { label: '代码案例', icon: DataAnalysis, color: '#909399' },
  image: { label: '图片', icon: Picture, color: '#B37FEB' }
}

const typeInfo = computed(() => typeMap[props.resource.type] || { label: '其他', icon: Document, color: '#909399' })
const typeLabel = computed(() => typeInfo.value.label)
const iconComponent = computed(() => typeInfo.value.icon)
const iconBg = computed(() => `${typeInfo.value.color}20`)

const formatTime = (time) => {
  if (!time) return '未知'
  const date = new Date(time)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}
</script>

<style scoped>
.resource-card {
  height: 100%;
  transition: all 0.3s ease;
  border-radius: 12px;
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.resource-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.resource-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #409EFF;
}

.resource-info {
  flex: 1;
}

.resource-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 4px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.resource-type {
  font-size: 12px;
  color: #67C23A;
  background: #E8F5E9;
  padding: 2px 8px;
  border-radius: 4px;
}

.card-body {
  margin-bottom: 12px;
}

.resource-desc {
  font-size: 13px;
  color: #606266;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin: 0;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #EBEEF5;
}

.create-time {
  font-size: 12px;
  color: #909399;
}

.actions {
  display: flex;
  gap: 8px;
}

.actions :deep(.el-button) {
  color: #909399;
}

.actions :deep(.el-button:hover) {
  color: #409EFF;
}
</style>