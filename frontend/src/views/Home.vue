<template>
  <div class="home-container">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="gradient-text">AI智学助手</span>
        </h1>
        <p class="hero-desc">
          基于大模型的个性化资源生成与学习多智能体系统
        </p>
        <div class="hero-stats">
          <div class="stat-item">
            <div class="stat-value">500+</div>
            <div class="stat-label">学习资源</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">100+</div>
            <div class="stat-label">学生画像</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">98%</div>
            <div class="stat-label">满意度</div>
          </div>
        </div>
        <div class="hero-buttons">
          <el-button type="primary" size="large" @click="goTo('/portrait')">
            <el-icon><User /></el-icon>
            开始构建画像
          </el-button>
          <el-button size="large" @click="goTo('/resource')">
            <el-icon><MagicStick /></el-icon>
            生成学习资源
          </el-button>
        </div>
      </div>
      <div class="hero-visual">
        <div class="floating-card card-1">
          <el-icon size="32" color="#409EFF"><Cpu /></el-icon>
          <span>智能画像</span>
        </div>
        <div class="floating-card card-2">
          <el-icon size="32" color="#67C23A"><Notebook /></el-icon>
          <span>知识图谱</span>
        </div>
        <div class="floating-card card-3">
          <el-icon size="32" color="#E6A23C"><TrendCharts /></el-icon>
          <span>学习路径</span>
        </div>
        <div class="floating-card card-4">
          <el-icon size="32" color="#F56C6C"><VideoPlay /></el-icon>
          <span>多模态资源</span>
        </div>
      </div>
    </div>
    
    <div class="features-section">
      <h2 class="section-title">核心功能</h2>
      <div class="features-grid">
        <el-card class="feature-card" hover>
          <div class="feature-icon bg-blue">
            <el-icon size="36"><User /></el-icon>
          </div>
          <h3 class="feature-title">对话式学生画像</h3>
          <p class="feature-desc">通过自然语言对话自动构建包含知识基础、认知风格、学习目标等多维度的动态学生画像</p>
        </el-card>
        
        <el-card class="feature-card" hover>
          <div class="feature-icon bg-green">
            <el-icon size="36"><MagicStick /></el-icon>
          </div>
          <h3 class="feature-title">多智能体资源生成</h3>
          <p class="feature-desc">多智能体协同生成专业课程讲解、思维导图、题库练习、实操案例等多种类型学习资源</p>
        </el-card>
        
        <el-card class="feature-card" hover>
          <div class="feature-icon bg-orange">
            <el-icon size="36"><TrendCharts /></el-icon>
          </div>
          <h3 class="feature-title">个性化学习路径</h3>
          <p class="feature-desc">基于学生画像智能规划学习路径，实时追踪学习进度，动态调整学习计划</p>
        </el-card>
        
        <el-card class="feature-card" hover>
          <div class="feature-icon bg-purple">
            <el-icon size="36"><Notebook /></el-icon>
          </div>
          <h3 class="feature-title">智能知识库管理</h3>
          <p class="feature-desc">支持PDF文档上传、自动切片入库、语义检索，构建专属知识图谱</p>
        </el-card>
      </div>
    </div>
    
    <div class="quick-actions">
      <h2 class="section-title">快速入口</h2>
      <div class="action-grid">
        <el-button
          v-for="action in quickActions"
          :key="action.path"
          class="action-btn"
          @click="goTo(action.path)"
        >
          <el-icon :size="24">{{ action.icon }}</el-icon>
          <span>{{ action.label }}</span>
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { User, MagicStick, TrendCharts, Notebook, Cpu, VideoPlay } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const quickActions = [
  { path: '/portrait', label: '学生画像', icon: User },
  { path: '/rag', label: '知识库', icon: Notebook },
  { path: '/resource', label: '资源生成', icon: MagicStick },
  { path: '/study', label: '学习路径', icon: TrendCharts }
]

const goTo = (path) => {
  router.push(path)
}
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.hero-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.hero-content {
  flex: 1;
  max-width: 50%;
}

.hero-title {
  font-size: 42px;
  font-weight: 700;
  margin: 0 0 16px 0;
}

.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-desc {
  font-size: 16px;
  color: #606266;
  margin: 0 0 24px 0;
  line-height: 1.6;
}

.hero-stats {
  display: flex;
  gap: 40px;
  margin-bottom: 24px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #409EFF;
}

.stat-label {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}

.hero-buttons {
  display: flex;
  gap: 12px;
}

.hero-visual {
  flex: 1;
  position: relative;
  height: 300px;
}

.floating-card {
  position: absolute;
  background: white;
  padding: 16px 20px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  animation: float 3s ease-in-out infinite;
}

.card-1 {
  top: 20px;
  left: 20px;
  animation-delay: 0s;
}

.card-2 {
  top: 100px;
  right: 40px;
  animation-delay: 0.75s;
}

.card-3 {
  bottom: 60px;
  left: 60px;
  animation-delay: 1.5s;
}

.card-4 {
  bottom: 20px;
  right: 20px;
  animation-delay: 2.25s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.features-section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #fff;
  margin: 0 0 20px 0;
  text-align: center;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.feature-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  border: none;
  padding: 24px;
  text-align: center;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  width: 72px;
  height: 72px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  color: white;
}

.bg-blue { background: linear-gradient(135deg, #667eea 0%, #409EFF 100%); }
.bg-green { background: linear-gradient(135deg, #84fab0 0%, #67C23A 100%); }
.bg-orange { background: linear-gradient(135deg, #ffecd2 0%, #E6A23C 100%); }
.bg-purple { background: linear-gradient(135deg, #a8edea 0%, #B37FEB 100%); }

.feature-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 12px 0;
}

.feature-desc {
  font-size: 13px;
  color: #606266;
  line-height: 1.6;
  margin: 0;
}

.quick-actions {
  margin-bottom: 24px;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.action-btn {
  background: rgba(255, 255, 255, 0.95);
  border: none;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #303133;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  background: white;
}
</style>