import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: '',
        userInfo: null
    }),
  
    getters: {
        isLogin: (state) => Boolean(state.token)
    },
  
    actions: {
        setLoginInfo(token, userInfo) {
            this.token = token
            this.userInfo = userInfo
        },
  
        clearLoginInfo() {
            this.token = ''
            this.userInfo = null
        }
    },
  
    persist: true
})