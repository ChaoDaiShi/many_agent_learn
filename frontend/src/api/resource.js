import request from './request'

export const generateResource = (data) => {
  return request.post('/gen/resource', data)
}

export const getResourceList = (page = 1, size = 10) => {
  return request.get('/gen/resources', { params: { page, size } })
}

export const getResourceDetail = (resourceId) => {
  return request.get(`/gen/resource/${resourceId}`)
}

export const deleteResource = (resourceId) => {
  return request.delete(`/gen/resource/${resourceId}`)
}

export const regenerateResource = (resourceId, data) => {
  return request.put(`/gen/resource/${resourceId}`, data)
}

export const getResourceTypes = () => {
  return request.get('/gen/types')
}