<template>
<div v-if="isLoading">Page is loading...</div>
<div v-else>
  <span>Logged in as {{user.name}}#{{user.discriminator}}</span>
</div>
</template>

<script>
import apiMixin from '@/mixins/apiMixin.js'

export default {
  mixins: [
    apiMixin
  ],

  data() {
    return {
      isLoading: true,
      user: null
    }
  },

  methods: {
    async fetchUser() {
      let data = await this.apiGet('/get_user');
      if (! data) { return }
      this.user = data;
      this.isLoading = false;
    }
  },

  mounted() {
    this.fetchUser();
  }
}
</script>

<style>
</style>