import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref(null)
  const studentId = ref('default_student')
  const portrait = ref(null)

  const isLoggedIn = computed(() => !!currentUser.value)

  const setUser = (user) => {
    currentUser.value = user
  }

  const setStudentId = (id) => {
    studentId.value = id
  }

  const setPortrait = (data) => {
    portrait.value = data
  }

  const logout = () => {
    currentUser.value = null
    studentId.value = 'default_student'
    portrait.value = null
    localStorage.removeItem('token')
  }

  return {
    currentUser,
    studentId,
    portrait,
    isLoggedIn,
    setUser,
    setStudentId,
    setPortrait,
    logout
  }
})