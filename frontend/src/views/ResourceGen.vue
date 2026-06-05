<template>
  <div class="resource-container">
    <div class="resource-header">
      <h2>多智能体资源生成</h2>
      <p>基于学生画像和学习需求，生成个性化学习资源</p>
    </div>
    
    <div class="resource-content">
      <div class="config-section">
        <el-card title="生成配置">
          <el-form :model="genConfig" label-width="120px">
            <el-form-item label="资源类型">
              <el-select v-model="genConfig.type" placeholder="请选择资源类型">
                <el-option label="专业课程讲解" value="document" />
                <el-option label="知识点思维导图" value="mindmap" />
                <el-option label="练习题库" value="questions" />
                <el-option label="多模态视频" value="video" />
                <el-option label="代码实操案例" value="code" />
                <el-option label="拓展阅读材料" value="reading" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="专业">
              <el-input v-model="genConfig.major" placeholder="请输入专业" />
            </el-form-item>
            
            <el-form-item label="课程名称">
              <el-input v-model="genConfig.course" placeholder="请输入课程名称" />
            </el-form-item>
            
            <el-form-item label="知识点">
              <el-input v-model="genConfig.topic" placeholder="请输入要生成的知识点" />
            </el-form-item>
            
            <el-form-item label="难度级别">
              <el-select v-model="genConfig.difficulty" placeholder="请选择难度">
                <el-option label="入门" value="beginner" />
                <el-option label="基础" value="basic" />
                <el-option label="进阶" value="intermediate" />
                <el-option label="高级" value="advanced" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="额外要求">
              <el-textarea v-model="genConfig.requirement" placeholder="请输入额外要求或说明" :rows="3" />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="generateResource" :disabled="isGenerating">
                <el-icon v-if="isGenerating"><Loading /></el-icon>
                {{ isGenerating ? '生成中...' : '生成资源' }}
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </div>
      
      <div class="result-section">
        <el-card title="生成结果">
          <div v-if="generatedContent" class="result-content">
            <div class="result-header">
              <h4>{{ generatedContent.title }}</h4>
              <span class="result-type">{{ getTypeLabel(generatedContent.type) }}</span>
            </div>
            <div class="result-body">
              <SseStream :url="streamUrl" v-if="isStreaming" />
              <div v-else v-html="renderedContent" class="markdown-content"></div>
            </div>
            <div class="result-actions">
              <el-button size="small" @click="copyContent">
                <el-icon><CopyDocument /></el-icon>
                复制内容
              </el-button>
              <el-button size="small" @click="saveResource">
                <el-icon><Download /></el-icon>
                保存资源
              </el-button>
            </div>
          </div>
          
          <div v-else class="empty-result">
            <el-icon size="48" color="#909399"><Document /></el-icon>
            <p>配置生成参数后点击生成按钮</p>
          </div>
        </el-card>
      </div>
      
      <div class="history-section">
        <el-card title="生成历史">
          <div class="history-list">
            <div
              v-for="resource in resourceHistory"
              :key="resource.id"
              class="history-item"
              @click="loadResource(resource)"
            >
              <div class="history-icon" :style="{ background: getTypeColor(resource.type) + '20' }">
                <component :is="getTypeIcon(resource.type)" :size="20" :color="getTypeColor(resource.type)" />
              </div>
              <div class="history-info">
                <span class="history-title">{{ resource.title }}</span>
                <span class="history-time">{{ formatTime(resource.created_at) }}</span>
              </div>
              <el-icon class="history-arrow" size="16" color="#909399"><ArrowRight /></el-icon>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { Loading, CopyDocument, Download, ArrowRight, Document, Notebook, VideoPlay, DataAnalysis } from '@element-plus/icons-vue'
import MarkdownIt from 'markdown-it'
import SseStream from '@/components/SseStream.vue'
import { generateResource as apiGenerateResource, getResourceList } from '@/api/resource'

const md = new MarkdownIt({ html: true, linkify: true })

const genConfig = ref({
  type: '',
  major: '',
  course: '',
  topic: '',
  difficulty: 'basic',
  requirement: ''
})

const isGenerating = ref(false)
const isStreaming = ref(false)
const streamUrl = ref('')
const generatedContent = ref(null)
const resourceHistory = ref([])
const renderedContent = ref('')

watch(generatedContent, (content) => {
  if (content && content.content) {
    renderedContent.value = md.render(content.content)
  }
})

const typeMap = {
  document: { label: '文档', icon: Document, color: '#409EFF' },
  mindmap: { label: '思维导图', icon: Notebook, color: '#67C23A' },
  questions: { label: '题库', icon: Notebook, color: '#E6A23C' },
  video: { label: '视频', icon: VideoPlay, color: '#F56C6C' },
  code: { label: '代码案例', icon: DataAnalysis, color: '#909399' },
  reading: { label: '阅读材料', icon: Document, color: '#B37FEB' }
}

const getTypeLabel = (type) => typeMap[type]?.label || '其他'
const getTypeIcon = (type) => typeMap[type]?.icon || FileText
const getTypeColor = (type) => typeMap[type]?.color || '#909399'

const generateResource = async () => {
  if (!genConfig.value.type || !genConfig.value.topic) {
    alert('请填写资源类型和知识点')
    return
  }
  
  isGenerating.value = true
  isStreaming.value = true
  
  try {
    const response = await apiGenerateResource(genConfig.value)
    
    if (response.task_id) {
      streamUrl.value = `/api/gen/stream/${response.task_id}`
    } else {
      generatedContent.value = response
      isStreaming.value = false
    }
    
    loadHistory()
  } catch (error) {
    console.error('Generation failed:', error)
    isStreaming.value = false
  } finally {
    isGenerating.value = false
  }
}

const loadResource = (resource) => {
  generatedContent.value = resource
}

const copyContent = () => {
  if (generatedContent.value?.content) {
    navigator.clipboard.writeText(generatedContent.value.content)
    alert('已复制到剪贴板')
  }
}

const saveResource = () => {
  console.log('Save resource:', generatedContent.value)
}

const formatTime = (time) => {
  if (!time) return '未知'
  const date = new Date(time)
  return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
}

const loadHistory = async () => {
  try {
    const response = await getResourceList(1, 10)
    resourceHistory.value = response.data
  } catch (error) {
    console.error('Failed to load history:', error)
  }
}

onMounted(() => {
  loadHistory()
})
</script>

<style scoped>
.resource-container {
  padding: 20px;
}

.resource-header {
  margin-bottom: 20px;
}

.resource-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #fff;
  margin: 0 0 8px 0;
}

.resource-header p {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
}

.resource-content {
  display: grid;
  grid-template-columns: 320px 1fr 300px;
  gap: 20px;
}

.config-section {
  grid-column: span 1;
}

.result-section {
  grid-column: span 1;
}

.history-section {
  grid-column: span 1;
}

.empty-result {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #909399;
}

.empty-result p {
  margin-top: 12px;
  font-size: 14px;
}

.result-content {
  background: #FAFAFA;
  border-radius: 8px;
  padding: 16px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.result-header h4 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.result-type {
  font-size: 12px;
  color: #67C23A;
  background: #E8F5E9;
  padding: 4px 12px;
  border-radius: 4px;
}

.result-body {
  min-height: 300px;
  font-size: 14px;
  line-height: 1.8;
}

.markdown-content {
  color: #303133;
}

.markdown-content :deep(h1) { font-size: 20px; font-weight: 600; margin: 16px 0 12px; padding-bottom: 8px; border-bottom: 1px solid #EBEEF5; }
.markdown-content :deep(h2) { font-size: 16px; font-weight: 600; margin: 12px 0 8px; }
.markdown-content :deep(h3) { font-size: 14px; font-weight: 600; margin: 10px 0 6px; }
.markdown-content :deep(p) { margin: 8px 0; }
.markdown-content :deep(ul), .markdown-content :deep(ol) { padding-left: 24px; margin: 8px 0; }
.markdown-content :deep(code) { background: #fff; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 12px; }
.markdown-content :deep(pre) { background: #1F2937; color: #E5E7EB; padding: 12px; border-radius: 8px; overflow-x: auto; }
.markdown-content :deep(pre code) { background: none; padding: 0; }
.markdown-content :deep(blockquote) { border-left: 4px solid #409EFF; padding: 8px 12px; background: #F5F7FA; border-radius: 0 4px 4px 0; color: #606266; }

.result-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #EBEEF5;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #FAFAFA;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.history-item:hover {
  background: #F0F5FF;
}

.history-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.history-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.history-title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.history-time {
  font-size: 12px;
  color: #909399;
}
</style>