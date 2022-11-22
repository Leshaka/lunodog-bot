<template>
  <div> Oauth2page </div>
</template>

<script>
import apiMixin from '@/mixins/apiMixin.js'

export default {
  mixins: [
    apiMixin
  ],

  methods: {
    async auth(code) {
      const resp = await this.apiPost('/oauth', {'code': code});
      if (resp) {
        this.$router.push({name: 'mainPage'});
      }
    }
  },

  mounted() {
    console.log(this.$route.query.code);
    if (!this.$route.query.code) {
      this.$router.push({name: 'errorPage', params: {'title': 'Auth Error', 'body': 'Missing Oauth2 code.'}});
      return;
    }
    this.auth(this.$route.query.code);
  }
}
</script>

<style></style>