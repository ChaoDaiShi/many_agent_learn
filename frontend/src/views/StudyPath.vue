<template>
  <div class="study-container">
    <div class="study-header">
      <h2>个性化学习路径</h2>
      <p>基于学生画像智能规划学习路径</p>
    </div>
    
    <div class="study-content">
      <div class="path-section">
        <el-card title="学习路径">
          <div class="path-header">
            <span>当前进度</span>
            <el-button size="small" @click="generatePath">
              <el-icon><Refresh /></el-icon>
              重新生成
            </el-button>
          </div>
          
          <div v-if="studyPath" class="path-content">
            <div class="path-progress">
              <el-progress :percentage="overallProgress" :color="progressColor" />
              <span class="progress-text">已完成 {{ completedSteps }}/{{ studyPath.steps.length }} 步</span>
            </div>
            
            <div class="steps-list">
              <div
                v-for="(step, index) in studyPath.steps"
                :key="index"
                :class="['step-item', { active: currentStep === index, completed: index < currentStep }]"
              >
                <div class="step-number">
                  <el-icon v-if="index < currentStep" color="#67C23A"><CheckCircle /></el-icon>
                  <span v-else>{{ index + 1 }}</span>
                </div>
                <div class="step-content">
                  <h4>{{ step.title }}</h4>
                  <p class="step-desc">{{ step.description }}</p>
                  <div class="step-meta">
                    <span class="step-duration">{{ step.duration }}分钟</span>
                    <span class="step-resource">{{ step.resource_type }}</span>
                  </div>
                </div>
                <div class="step-action">
                  <el-button
                    v-if="index === currentStep"
                    type="primary"
                    size="small"
                    @click="markStepComplete(index)"
                  >
                    开始学习
                  </el-button>
                  <span v-else-if="index < currentStep" class="completed-text">已完成</span>
                </div>
              </div>
            </div>
          </div>
          
          <div v-else class="empty-path">
            <el-icon size="48" color="#909399"><Route /></el-icon>
            <p>点击重新生成按钮生成学习路径</p>
          </div>
        </el-card>
      </div>
      
      <div class="wrong-section">
        <el-card title="错题本">
          <div class="wrong-header">
            <span>共 {{ wrongQuestions.length }} 道错题</span>
            <el-button size="small" @click="addWrongQuestion">
              <el-icon><Plus /></el-icon>
              添加错题
            </el-button>
          </div>
          
          <div class="wrong-list">
            <div v-for="question in wrongQuestions" :key="question.id" class="wrong-item">
              <div class="wrong-info">
                <h4>{{ question.title }}</h4>
                <p class="wrong-desc">{{ question.content }}</p>
                <div class="wrong-meta">
                  <span class="wrong-subject">{{ question.subject }}</span>
                  <span class="wrong-count">错误 {{ question.error_count }} 次</span>
                </div>
              </div>
              <div class="wrong-action">
                <el-button size="small" text @click="viewQuestion(question)">
                  <el-icon><View /></el-icon>
                </el-button>
                <el-button size="small" text @click="deleteWrongQuestion(question.id)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
        </el-card>
      </div>
      
      <div class="stats-section">
        <el-card title="学习统计">
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon bg-blue">
                <el-icon size="24"><Clock /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ totalStudyTime }}</div>
                <div class="stat-label">总学习时长(分钟)</div>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon bg-green">
                <el-icon size="24"><Aim /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ completedCourses }}</div>
                <div class="stat-label">已完成课程</div>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon bg-orange">
                <el-icon size="24"><TrendCharts /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ accuracyRate }}%</div>
                <div class="stat-label">答题正确率</div>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon bg-purple">
                <el-icon size="24"><Trophy /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ learningStreak }}</div>
                <div class="stat-label">连续学习天数</div>
              </div>
            </div>
          </div>
        </el-card>
        
        <el-card title="学习建议">
          <div class="suggestions">
            <div v-for="(suggestion, index) in suggestions" :key="index" class="suggestion-item">
              <el-icon :color="suggestion.color" size="16">{{ suggestion.icon }}</el-icon>
              <span>{{ suggestion.text }}</span>
            </div>
          </div>
        </el-card>
      </div>
    </div>
    
    <el-dialog title="添加错题" :visible.sync="showAddDialog">
      <el-form :model="newQuestion" label-width="80px">
        <el-form-item label="题目">
          <el-input v-model="newQuestion.title" placeholder="输入题目标题" />
        </el-form-item>
        <el-form-item label="内容">
          <el-textarea v-model="newQuestion.content" placeholder="输入题目内容" :rows="3" />
        </el-form-item>
        <el-form-item label="科目">
          <el-input v-model="newQuestion.subject" placeholder="输入科目" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="submitNewQuestion">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Refresh, MapLocation, Plus, View, Delete, Clock, Aim, TrendCharts, Trophy, Warning, Lightning } from '@element-plus/icons-vue'
import { getStudyPath, generateStudyPath, getWrongQuestions, addWrongQuestion as addWQ, deleteWrongQuestion as deleteWQ } from '@/api/study'

const studyPath = ref(null)
const currentStep = ref(0)
const wrongQuestions = ref([])
const showAddDialog = ref(false)
const newQuestion = ref({ title: '', content: '', subject: '' })

const totalStudyTime = ref(1250)
const completedCourses = ref(12)
const accuracyRate = ref(85)
const learningStreak = ref(7)

const suggestions = ref([
  { icon: Warning, text: '建议重点复习数据结构章节，近期错误较多', color: '#F56C6C' },
  { icon: Lightning, text: '今天的学习任务已完成，继续保持！', color: '#E6A23C' },
  { icon: Lightning, text: '建议增加实操练习时间，巩固知识', color: '#409EFF' }
])

const completedSteps = computed(() => currentStep.value)
const overallProgress = computed(() => {
  if (!studyPath.value?.steps?.length) return 0
  return Math.round((currentStep.value / studyPath.value.steps.length) * 100)
})
const progressColor = computed(() => {
  if (overallProgress.value >= 80) return '#67C23A'
  if (overallProgress.value >= 50) return '#E6A23C'
  return '#409EFF'
})

const generatePath = async () => {
  try {
    const response = await generateStudyPath('default_student', {
      target: 'complete',
      duration: 30
    })
    studyPath.value = response.data
    currentStep.value = 0
  } catch (error) {
    console.error('Failed to generate path:', error)
  }
}

const markStepComplete = (index) => {
  if (index === currentStep.value && index < (studyPath.value?.steps?.length || 0)) {
    currentStep.value++
  }
}

const loadWrongQuestions = async () => {
  try {
    const response = await getWrongQuestions('default_student')
    wrongQuestions.value = response.data
  } catch (error) {
    console.error('Failed to load wrong questions:', error)
  }
}

const addWrongQuestion = () => {
  showAddDialog.value = true
}

const submitNewQuestion = async () => {
  if (!newQuestion.value.title) return
  
  try {
    await addWQ({
      ...newQuestion.value,
      student_id: 'default_student',
      error_count: 1
    })
    loadWrongQuestions()
    showAddDialog.value = false
    newQuestion.value = { title: '', content: '', subject: '' }
  } catch (error) {
    console.error('Failed to add question:', error)
  }
}

const viewQuestion = (question) => {
  console.log('View question:', question)
}

const deleteWrongQuestion = async (questionId) => {
  try {
    await deleteWQ(questionId)
    loadWrongQuestions()
  } catch (error) {
    console.error('Failed to delete question:', error)
  }
}

generatePath()
loadWrongQuestions()
</script>

<style scoped>
.study-container {
  padding: 20px;
}

.study-header {
  margin-bottom: 20px;
}

.study-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #fff;
  margin: 0 0 8px 0;
}

.study-header p {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
}

.study-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.path-section {
  grid-column: span 1;
}

.wrong-section {
  grid-column: span 1;
}

.stats-section {
  grid-column: span 2;
}

.path-header,
.wrong-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.path-header span,
.wrong-header span {
  font-size: 14px;
  color: #606266;
}

.path-progress {
  margin-bottom: 20px;
}

.progress-text {
  display: block;
  text-align: right;
  font-size: 13px;
  color: #606266;
  margin-top: 8px;
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.step-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: #FAFAFA;
  border-radius: 12px;
  border-left: 4px solid #D9D9D9;
  transition: all 0.3s ease;
}

.step-item.completed {
  border-left-color: #67C23A;
  background: #F0FFF0;
}

.step-item.active {
  border-left-color: #409EFF;
  background: #F0F5FF;
}

.step-number {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #E4E7ED;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  color: #606266;
  flex-shrink: 0;
}

.step-item.completed .step-number {
  background: #E8F5E9;
}

.step-content {
  flex: 1;
}

.step-content h4 {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 4px 0;
}

.step-desc {
  font-size: 13px;
  color: #606266;
  margin: 0 0 8px 0;
}

.step-meta {
  display: flex;
  gap: 12px;
}

.step-duration,
.step-resource {
  font-size: 12px;
  color: #909399;
  background: #fff;
  padding: 2px 8px;
  border-radius: 4px;
}

.step-action {
  flex-shrink: 0;
}

.completed-text {
  font-size: 13px;
  color: #67C23A;
  font-weight: 500;
}

.empty-path {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #909399;
}

.empty-path p {
  margin-top: 12px;
  font-size: 14px;
}

.wrong-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.wrong-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: #FEF5F5;
  border-radius: 8px;
}

.wrong-info {
  flex: 1;
}

.wrong-info h4 {
  font-size: 14px;
  font-weight: 600;
  color: #F56C6C;
  margin: 0 0 4px 0;
}

.wrong-desc {
  font-size: 13px;
  color: #606266;
  margin: 0 0 8px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.wrong-meta {
  display: flex;
  gap: 12px;
}

.wrong-subject {
  font-size: 12px;
  color: #67C23A;
  background: #E8F5E9;
  padding: 2px 8px;
  border-radius: 4px;
}

.wrong-count {
  font-size: 12px;
  color: #F56C6C;
}

.wrong-action {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #FAFAFA;
  border-radius: 8px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.bg-blue { background: linear-gradient(135deg, #667eea 0%, #409EFF 100%); }
.bg-green { background: linear-gradient(135deg, #84fab0 0%, #67C23A 100%); }
.bg-orange { background: linear-gradient(135deg, #ffecd2 0%, #E6A23C 100%); }
.bg-purple { background: linear-gradient(135deg, #a8edea 0%, #B37FEB 100%); }

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #303133;
}

.stat-label {
  font-size: 12px;
  color: #909399;
}

.suggestions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: #FFFBE6;
  border-radius: 8px;
  font-size: 13px;
  color: #8A6D3B;
}
</style>