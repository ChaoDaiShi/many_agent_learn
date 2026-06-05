<template>
  <div class="rag-container">
    <div class="rag-header">
      <h2>知识库管理</h2>
      <p>上传PDF文档构建您的专属知识库</p>
    </div>
    
    <div class="rag-content">
      <div class="upload-section">
        <el-card title="上传文档">
          <UploadPdf @upload-success="handleUploadSuccess" />
        </el-card>
      </div>
      
      <div class="search-section">
        <el-card title="知识库检索">
          <div class="search-box">
            <el-input
              v-model="searchQuery"
              placeholder="输入关键词检索知识库..."
              @keyup.enter="searchKnowledge"
            />
            <el-button type="primary" @click="searchKnowledge">
              <el-icon><Search /></el-icon>
              检索
            </el-button>
          </div>
          
          <div v-if="searchResults.length > 0" class="search-results">
            <h4>检索结果</h4>
            <div v-for="(result, index) in searchResults" :key="index" class="result-item">
              <div class="result-header">
                <span class="result-title">{{ result.title }}</span>
                <span class="result-score">相似度: {{ (result.score * 100).toFixed(1) }}%</span>
              </div>
              <p class="result-content">{{ result.content }}</p>
            </div>
          </div>
        </el-card>
      </div>
      
      <div class="document-section">
        <el-card title="文档列表">
          <div class="document-header">
            <span>共 {{ documentList.length }} 个文档</span>
            <el-button size="small" @click="refreshDocuments">
              <el-icon><RefreshCw /></el-icon>
              刷新
            </el-button>
          </div>
          
          <el-table :data="documentList" border>
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column prop="name" label="文档名称" />
            <el-table-column prop="size" label="大小" width="100" />
            <el-table-column prop="chunk_count" label="切片数" width="100" />
            <el-table-column prop="created_at" label="上传时间" width="180" />
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" text @click="viewDocument(scope.row)">
                  <el-icon><View /></el-icon>
                  查看
                </el-button>
                <el-button size="small" text @click="deleteDocument(scope.row.id)">
                  <el-icon><Delete /></el-icon>
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <el-pagination
            v-if="total > 0"
            :current-page="page"
            :page-size="pageSize"
            :total="total"
            @current-change="handlePageChange"
            layout="prev, pager, next"
          />
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, Refresh, View, Delete } from '@element-plus/icons-vue'
import UploadPdf from '@/components/UploadPdf.vue'
import { getDocumentList, queryDocument, deleteDocument as deleteDoc } from '@/api/rag'

const documentList = ref([])
const searchQuery = ref('')
const searchResults = ref([])
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

const loadDocuments = async () => {
  try {
    const response = await getDocumentList(page.value, pageSize.value)
    documentList.value = response.data
    total.value = response.total
  } catch (error) {
    console.error('Failed to load documents:', error)
  }
}

const handleUploadSuccess = () => {
  loadDocuments()
}

const searchKnowledge = async () => {
  if (!searchQuery.value.trim()) return
  
  try {
    const response = await queryDocument(searchQuery.value)
    searchResults.value = response.data
  } catch (error) {
    console.error('Search failed:', error)
  }
}

const viewDocument = (doc) => {
  console.log('View document:', doc)
}

const deleteDocument = async (docId) => {
  try {
    await deleteDoc(docId)
    loadDocuments()
  } catch (error) {
    console.error('Delete failed:', error)
  }
}

const refreshDocuments = () => {
  loadDocuments()
}

const handlePageChange = (newPage) => {
  page.value = newPage
  loadDocuments()
}

onMounted(() => {
  loadDocuments()
})
</script>

<style scoped>
.rag-container {
  padding: 20px;
}

.rag-header {
  margin-bottom: 20px;
}

.rag-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #fff;
  margin: 0 0 8px 0;
}

.rag-header p {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
}

.rag-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.upload-section,
.search-section {
  grid-column: span 1;
}

.document-section {
  grid-column: span 2;
}

.search-box {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.search-box :deep(.el-input) {
  flex: 1;
}

.search-results {
  max-height: 300px;
  overflow-y: auto;
}

.search-results h4 {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 12px 0;
}

.result-item {
  background: #F5F7FA;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 12px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.result-title {
  font-size: 14px;
  font-weight: 600;
  color: #409EFF;
}

.result-score {
  font-size: 12px;
  color: #67C23A;
}

.result-content {
  font-size: 13px;
  color: #606266;
  line-height: 1.6;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.document-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.document-header span {
  font-size: 14px;
  color: #606266;
}
</style>