import request from './request'

export const getStudentPortrait = (studentId) => {
  return request.get(`/student/portrait/${studentId}`)
}

export const createPortrait = (data) => {
  return request.post('/student/portrait', data)
}

export const updatePortrait = (studentId, data) => {
  return request.put(`/student/portrait/${studentId}`, data)
}

export const deletePortrait = (studentId) => {
  return request.delete(`/student/portrait/${studentId}`)
}

export const chatWithPortrait = (studentId, message) => {
  return request.post(`/student/chat/${studentId}`, { message })
}

export const getPortraitList = (page = 1, size = 10) => {
  return request.get('/student/portrait', { params: { page, size } })
}