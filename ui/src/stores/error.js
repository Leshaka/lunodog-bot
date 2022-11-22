import { defineStore } from 'pinia'

export const useErrorStore = defineStore('error',  {
  state: () => {
    return {
      title: 'Error',
      body: 'Unknown error'
    }
  }
})
