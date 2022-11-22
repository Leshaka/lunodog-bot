<template>
  <div class="layout">
    <div class="title"> {{ errorStore.title }} </div>
    <div class="body"> {{ errorStore.body }} </div>
    <div class="button" @click="$router.back()"> Go Back </div>
  </div>
</template>

<script>
import { useErrorStore } from '@/stores/error'

export default {
  setup() {
    const errorStore = useErrorStore();
    return { errorStore }
  }
}

</script>

<style scoped lang="scss">
.layout {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  min-width: 100%;
  min-height: 100vh;
  background: var(--bgc2);
}

.title {
  color: #fc462a;
  font-size: 48px;
  font-family: oswald;
  letter-spacing: 1px;
  margin-bottom: 25px;
}

.body {
  color: var(--fontNormal);
  font-family: roboto;
  font-size: 20px;
}

.button {
  background: #6C89E0;
  padding: 10px 20px 10px 20px;
  border-radius: 10px;
  color: white;
  cursor: pointer;
  margin-top: 20px;
  font-family: roboto;
}
</style>