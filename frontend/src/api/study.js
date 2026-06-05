import request from './request'

export const getStudyPath = (studentId) => {
  return request.get(`/study/path/${studentId}`)
}

export const generateStudyPath = (studentId, data) => {
  return request.post(`/study/path/${studentId}`, data)
}

export const updateStudyPath = (pathId, data) => {
  return request.put(`/study/path/${pathId}`, data)
}

export const getWrongQuestions = (studentId, page = 1, size = 10) => {
  return request.get(`/study/wrong-questions/${studentId}`, { params: { page, size } })
}

export const addWrongQuestion = (data) => {
  return request.post('/study/wrong-question', data)
}

export const deleteWrongQuestion = (questionId) => {
  return request.delete(`/study/wrong-question/${questionId}`)
}

export const getProgress = (studentId) => {
  return request.get(`/study/progress/${studentId}`)
}

export const updateProgress = (studentId, data) => {
  return request.put(`/study/progress/${studentId}`, data)
}