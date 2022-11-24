<template>
  <div class="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  inject: ["$staticPath"]
}
</script>

<style lang="scss">

body {
  all: initial;
  *:not(path) {
    all: unset;
    box-sizing: border-box;
  }

  path {
    box-sizing: content-box;
  }
}

@font-face {
  font-family: oswald;
  src: url("@/../public/fonts/OswaldFont/Oswald-Regular.ttf");
}

@font-face {
  font-family: oswald-light;
  src: url("@/../public/fonts/OswaldFont/Oswald-Light.ttf");
}

@font-face {
  font-family: roboto;
  src: url("@/../public/fonts/Roboto/Roboto-Regular.ttf");
}

@font-face {
  font-family: roboto-light;
  src: url("@/../public/fonts/Roboto/Roboto-Light.ttf");
}

@font-face {
  font-family: roboto-bold;
  src: url("@/../public/fonts/Roboto/Roboto-Bold.ttf");
}

@font-face {
  font-family: holtwood;
  src: url("@/../public/fonts/Holtwood_One_SC/HoltwoodOneSC-Regular.ttf");
}

</style>
