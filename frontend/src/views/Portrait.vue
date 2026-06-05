<template>
  <div class="portrait-container">
    <div class="portrait-layout">
      <div class="chat-panel">
        <div class="chat-header">
          <h2>学生画像对话</h2>
          <p class="subtitle">通过对话构建您的专属学习画像</p>
        </div>
        
        <div class="chat-messages" ref="messagesContainer">
          <div v-for="msg in messages" :key="msg.id" :class="['message-item', msg.role]">
            <div class="avatar">
              <el-icon v-if="msg.role === 'user'" size="24"><User /></el-icon>
              <el-icon v-else size="24" color="#409EFF"><Bot /></el-icon>
            </div>
            <div class="message-content">
              <p>{{ msg.content }}</p>
            </div>
          </div>
          
          <div v-if="loading" class="loading-message">
            <el-icon class="loading" size="20"><Loading /></el-icon>
            <span>正在分析...</span>
          </div>
        </div>
        
        <div class="chat-input">
          <el-input
            v-model="inputMessage"
            placeholder="请输入您的专业、学习目标、兴趣爱好等信息..."
            @keyup.enter="sendMessage"
          />
          <el-button type="primary" @click="sendMessage">
            <el-icon><Message /></el-icon>
          </el-button>
        </div>
      </div>
      
      <div class="portrait-panel">
        <div class="panel-header">
          <h3>学生画像</h3>
          <el-button size="small" @click="refreshPortrait">
            <el-icon><Refresh /></el-icon>
            更新画像
          </el-button>
        </div>
        
        <div v-if="portrait" class="portrait-content">
          <div class="portrait-card">
            <h4>基本信息</h4>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">专业</span>
                <span class="value">{{ portrait.major || '未设置' }}</span>
              </div>
              <div class="info-item">
                <span class="label">年级</span>
                <span class="value">{{ portrait.grade || '未设置' }}</span>
              </div>
              <div class="info-item">
                <span class="label">学习目标</span>
                <span class="value">{{ portrait.learning_goal || '未设置' }}</span>
              </div>
              <div class="info-item">
                <span class="label">兴趣方向</span>
                <span class="value">{{ portrait.interests || '未设置' }}</span>
              </div>
            </div>
          </div>
          
          <div class="portrait-card">
            <h4>知识基础</h4>
            <div class="knowledge-list">
              <div v-for="(level, subject) in portrait.knowledge_base" :key="subject" class="knowledge-item">
                <span class="subject">{{ subject }}</span>
                <el-progress :percentage="level" :color="getLevelColor(level)" />
              </div>
            </div>
          </div>
          
          <div class="portrait-card">
            <h4>认知风格</h4>
            <div class="cognitive-traits">
              <div v-for="trait in portrait.cognitive_traits" :key="trait.name" class="trait-item">
                <span class="trait-name">{{ trait.name }}</span>
                <span class="trait-value">{{ trait.value }}</span>
              </div>
            </div>
          </div>
          
          <div class="portrait-card">
            <h4>学习偏好</h4>
            <div class="preferences">
              <el-tag
                v-for="pref in portrait.learning_preferences"
                :key="pref"
                type="info"
                size="small"
              >
                {{ pref }}
              </el-tag>
            </div>
          </div>
          
          <div class="portrait-card">
            <h4>易错点分析</h4>
            <div class="weak-points">
              <div v-for="(count, point) in portrait.weak_points" :key="point" class="weak-item">
                <span class="point-name">{{ point }}</span>
                <span class="point-count">错误 {{ count }} 次</span>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else class="empty-portrait">
          <el-icon size="48" color="#909399"><User /></el-icon>
          <p>开始对话以构建您的学生画像</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { User, Cpu, Loading, Message, Refresh } from '@element-plus/icons-vue'
import { chatWithPortrait, getStudentPortrait } from '@/api/student'

const messages = ref([
  { id: 1, role: 'assistant', content: '您好！我来帮您构建学生画像。请告诉我您的专业、年级、学习目标或者兴趣爱好等信息。' }
])
const inputMessage = ref('')
const loading = ref(false)
const portrait = ref(null)

const messagesContainer = ref(null)

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (!inputMessage.value.trim()) return
  
  messages.value.push({
    id: messages.value.length + 1,
    role: 'user',
    content: inputMessage.value
  })
  
  inputMessage.value = ''
  loading.value = true
  
  await scrollToBottom()
  
  try {
    const response = await chatWithPortrait('default_student', messages.value[messages.value.length - 1].content)
    
    messages.value.push({
      id: messages.value.length + 1,
      role: 'assistant',
      content: response.content
    })
    
    if (response.portrait) {
      portrait.value = response.portrait
    }
  } catch (error) {
    messages.value.push({
      id: messages.value.length + 1,
      role: 'assistant',
      content: '抱歉，我遇到了一些问题，请稍后重试。'
    })
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}

const refreshPortrait = async () => {
  try {
    const response = await getStudentPortrait('default_student')
    portrait.value = response.data
  } catch (error) {
    console.error('Failed to refresh portrait:', error)
  }
}

const getLevelColor = (level) => {
  if (level >= 80) return '#67C23A'
  if (level >= 60) return '#E6A23C'
  return '#F56C6C'
}
</script>

<style scoped>
.portrait-container {
  height: calc(100vh - 104px);
}

.portrait-layout {
  display: flex;
  height: 100%;
  gap: 20px;
}

.chat-panel {
  flex: 1;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.chat-header {
  padding: 20px;
  border-bottom: 1px solid #EBEEF5;
}

.chat-header h2 {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 4px 0;
}

.subtitle {
  font-size: 13px;
  color: #909399;
  margin: 0;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.message-item {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.message-item.user {
  flex-direction: row-reverse;
}

.message-item.user .message-content {
  background: #409EFF;
  color: white;
  border-radius: 12px 12px 0 12px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #F5F7FA;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  background: #F5F7FA;
  border-radius: 12px 12px 12px 0;
}

.message-content p {
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
}

.loading-message {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #409EFF;
  padding: 12px;
}

.loading {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.chat-input {
  padding: 16px;
  border-top: 1px solid #EBEEF5;
  display: flex;
  gap: 12px;
}

.chat-input :deep(.el-input) {
  flex: 1;
}

.portrait-panel {
  width: 400px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.panel-header {
  padding: 20px;
  border-bottom: 1px solid #EBEEF5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.portrait-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.portrait-card {
  background: #FAFAFA;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}

.portrait-card h4 {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 12px 0;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-item .label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.info-item .value {
  font-size: 13px;
  color: #303133;
  font-weight: 500;
}

.knowledge-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.knowledge-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.subject {
  font-size: 12px;
  color: #606266;
}

.cognitive-traits {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.trait-item {
  background: #E8F5E9;
  padding: 6px 12px;
  border-radius: 20px;
  display: flex;
  gap: 8px;
}

.trait-name {
  font-size: 12px;
  color: #67C23A;
  font-weight: 500;
}

.trait-value {
  font-size: 12px;
  color: #303133;
}

.preferences {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.weak-points {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.weak-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #FEF0F0;
  border-radius: 8px;
}

.point-name {
  font-size: 13px;
  color: #F56C6C;
}

.point-count {
  font-size: 12px;
  color: #909399;
}

.empty-portrait {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
}

.empty-portrait p {
  margin-top: 12px;
  font-size: 14px;
}
</style>