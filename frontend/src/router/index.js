import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Portrait from '../views/Portrait.vue'
import RagManage from '../views/RagManage.vue'
import ResourceGen from '../views/ResourceGen.vue'
import StudyPath from '../views/StudyPath.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/portrait',
    name: 'Portrait',
    component: Portrait
  },
  {
    path: '/rag',
    name: 'RagManage',
    component: RagManage
  },
  {
    path: '/resource',
    name: 'ResourceGen',
    component: ResourceGen
  },
  {
    path: '/study',
    name: 'StudyPath',
    component: StudyPath
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router