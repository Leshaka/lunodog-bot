import axios from 'axios'

import { useErrorStore } from '@/stores/error'

export default {
  inject: ["$apiURL"],

  methods: {

    async apiGet(path) {
      try {
        const response = await axios.get(this.$apiURL+path, {withCredentials: true});
        return response.data;
      } catch (e) {
        this.$_handleApiError(e);
      }
    },

    async apiPost(path, data) {
      try {
        const response = await axios.post(this.$apiURL+path, data, {withCredentials: true});
        return response.data;
      } catch (e) {
        this.$_handleApiError(e);
      }
    },

    $_handleApiError(e) {
      let errorData = {title: 'Unknown Error', body: ''}
      const errorStore = useErrorStore();

      // redirect to login page on not authed response
      if (e.response?.status == 401) {
        this.$router.push({name: 'loginPage'})
        return;
      }

      // recieved an error response directly from the api server
      else if (e.response?.data?.error) {
        errorData.title = e.response.data.error.status;
        errorData.body = e.response.data.error.message;
      }

      // received error from axios lib (such as unable to connect to host, etc)
      else if (e.name === 'AxiosError') {  
        errorData.title = 'API Error';
        errorData.body = e.message;
      }

      errorStore.$patch(errorData)
      this.$router.push({name: 'errorPage', query: errorData})
    }

  }
}