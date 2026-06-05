<template>
  <div class="app-container">
    <el-container>
      <el-header class="app-header">
        <div class="header-content">
          <div class="logo">
            <el-icon class="logo-icon" size="32" color="#409EFF">
              <Cpu />
            </el-icon>
            <span class="logo-text">AI智学助手</span>
          </div>
          <el-menu
            mode="horizontal"
            :default-active="currentRoute"
            class="nav-menu"
          >
            <el-menu-item index="/">
              <el-icon><HomeFilled /></el-icon>
              <span>首页</span>
            </el-menu-item>
            <el-menu-item index="/portrait">
              <el-icon><User /></el-icon>
              <span>学生画像</span>
            </el-menu-item>
            <el-menu-item index="/rag">
              <el-icon><Notebook /></el-icon>
              <span>知识库管理</span>
            </el-menu-item>
            <el-menu-item index="/resource">
              <el-icon><MagicStick /></el-icon>
              <span>资源生成</span>
            </el-menu-item>
            <el-menu-item index="/study">
              <el-icon><TrendCharts /></el-icon>
              <span>学习路径</span>
            </el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main class="app-main">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { Cpu, HomeFilled, User, Notebook, MagicStick, TrendCharts } from '@element-plus/icons-vue'

const router = useRouter()
const currentRoute = computed(() => router.currentRoute.value.path)
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.app-header {
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 0;
  height: 64px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 30px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.logo-text {
  font-size: 20px;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-menu {
  flex: 1;
  justify-content: center;
}

.nav-menu :deep(.el-menu-item) {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.nav-menu :deep(.el-menu-item.is-active) {
  color: #409EFF;
}

.app-main {
  padding: 20px;
  min-height: calc(100vh - 64px);
}
</style>