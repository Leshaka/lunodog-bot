<template>
  <div class="layout">
  <span class="title">Lunodog Web UI</span>
  <a class="button" :href="`${ $oauthURI }`">
    <span>Login with Discord</span>
    <img :src="`${ $staticPath }/img/discord.png`"/>
  </a>
</div>
</template>

<script>
export default {
  inject: ["$oauthURI", "$staticPath"],
}
</script>

<style scoped lang="scss">

  .layout {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    min-width: 100%;
    min-height: 100vh;
    background-color: var(--bgc2);
  }

  .title {
    margin-bottom: 10px;
    font-family: oswald;
    font-size: 24px;
    letter-spacing: 1px;
    color: white;
  }

  .button {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
  
    background: #6C89E0;
    padding: 10px 20px 10px 20px;
    border-radius: 10px;
    cursor: pointer;
    span {
      color: white;
      font-family: roboto;
      margin-right: 10px;
    }
  }

</style>