import { defineStore } from 'pinia'

export const useUserStore = defineStore('global',  {
  state: () => {
    return {
      selGuild: null,
      selModule: null
    }
  }
})
