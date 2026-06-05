import request from './request'

export const uploadPdf = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return request.post('/rag/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export const getDocumentList = (page = 1, size = 10) => {
  return request.get('/rag/documents', { params: { page, size } })
}

export const deleteDocument = (docId) => {
  return request.delete(`/rag/document/${docId}`)
}

export const queryDocument = (query, topK = 5) => {
  return request.post('/rag/query', { query, top_k: topK })
}

export const getDocumentDetail = (docId) => {
  return request.get(`/rag/document/${docId}`)
}