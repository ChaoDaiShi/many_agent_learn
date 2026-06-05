<template>
  <div class="sse-container">
    <div class="stream-content" v-html="renderedContent"></div>
    <div v-if="loading" class="loading-indicator">
      <el-icon class="loading-icon" size="20"><Loading /></el-icon>
      <span>正在生成中...</span>
    </div>
    <div v-if="error" class="error-message">
      <el-icon color="#F56C6C"><Warning /></el-icon>
      <span>{{ error }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted } from 'vue'
import { Loading, Warning } from '@element-plus/icons-vue'
import MarkdownIt from 'markdown-it'

const props = defineProps({
  url: {
    type: String,
    required: true
  },
  autoStart: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['complete', 'error'])

const content = ref('')
const loading = ref(false)
const error = ref('')

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true
})

const renderedContent = ref('')

watch(content, (newContent) => {
  renderedContent.value = md.render(newContent)
})

let eventSource = null

const connect = () => {
  if (eventSource) return
  
  loading.value = true
  error.value = ''
  content.value = ''
  
  eventSource = new EventSource(props.url)
  
  eventSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      if (data.type === 'content') {
        content.value += data.content
      } else if (data.type === 'complete') {
        loading.value = false
        eventSource.close()
        emit('complete', content.value)
      } else if (data.type === 'error') {
        error.value = data.message
        loading.value = false
        eventSource.close()
        emit('error', data.message)
      }
    } catch (e) {
      content.value += event.data
    }
  }
  
  eventSource.onerror = (e) => {
    error.value = '连接错误，请重试'
    loading.value = false
    if (eventSource) {
      eventSource.close()
      eventSource = null
    }
    emit('error', '连接错误')
  }
}

const disconnect = () => {
  if (eventSource) {
    eventSource.close()
    eventSource = null
  }
  loading.value = false
}

onUnmounted(() => {
  disconnect()
})

if (props.autoStart) {
  connect()
}

defineExpose({ connect, disconnect, content })
</script>

<style scoped>
.sse-container {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  min-height: 200px;
  position: relative;
}

.stream-content {
  font-size: 14px;
  line-height: 1.8;
  color: #303133;
}

.stream-content :deep(h1) {
  font-size: 20px;
  font-weight: 600;
  margin: 16px 0 12px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #EBEEF5;
}

.stream-content :deep(h2) {
  font-size: 16px;
  font-weight: 600;
  margin: 12px 0 8px 0;
}

.stream-content :deep(h3) {
  font-size: 14px;
  font-weight: 600;
  margin: 10px 0 6px 0;
}

.stream-content :deep(p) {
  margin: 8px 0;
}

.stream-content :deep(ul),
.stream-content :deep(ol) {
  padding-left: 24px;
  margin: 8px 0;
}

.stream-content :deep(li) {
  margin: 4px 0;
}

.stream-content :deep(code) {
  background: #F5F7FA;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 12px;
}

.stream-content :deep(pre) {
  background: #1F2937;
  color: #E5E7EB;
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 8px 0;
}

.stream-content :deep(pre code) {
  background: none;
  padding: 0;
  color: inherit;
}

.stream-content :deep(a) {
  color: #409EFF;
  text-decoration: none;
}

.stream-content :deep(a:hover) {
  text-decoration: underline;
}

.stream-content :deep(blockquote) {
  border-left: 4px solid #409EFF;
  padding-left: 12px;
  margin: 8px 0;
  color: #606266;
  background: #F5F7FA;
  padding: 8px 12px;
  border-radius: 0 4px 4px 0;
}

.loading-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  color: #409EFF;
  font-size: 14px;
}

.loading-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.error-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: #FEF0F0;
  color: #F56C6C;
  border-radius: 4px;
  margin-top: 12px;
}
</style>