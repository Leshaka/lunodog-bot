<template>
  <div class="layout">
    <!-- upper part -->
    <div class="upper">
      <div class="menu"><a>Github</a><a>Support</a></div>
      <div class="title">
        <span>LUNODOG</span>
        <span class="description">
  Lunodog is a multi-purpose open source discord bot with modular design made for #promode.ru community.
        </span>
      </div>
      <a class="button" :href="`${ $oauthURI }`">
        <span>Login with Discord</span>
        <img src="/img/discord.png"/>
      </a>
      <div class="waves-container">
        <svg viewBox="0 0 1920 230">
          <path d="m -1.0247443,133.81929 c 0,0 160.9084243,-126.236484 253.0761343,-115.745444 79.73464,9.07584 112.43202,129.648754 190.83295,146.774114 43.93689,9.5975 86.81939,-25.07056 131.50232,-30.16896 65.82741,-7.51127 134.07144,13.9638 198.76346,-0.3406 52.77805,-11.67003 93.37726,-73.529771 147.15835,-68.116181 72.76631,7.32447 103.68073,133.196041 176.74463,129.994541 84.564,-3.7056 175.3465,-69.55096 285.2358,-44.0824 96.9281,22.4648 169.731,-133.756264 269.1203,-129.118794 51.2665,2.39209 83.2103,63.351293 132.0116,79.238434 44.0337,14.33493 138.3765,12.3281 138.3765,12.3281 l -1.5443,51.84346 1.8042,63.8541 -1923.0751843,0.5644 z"/>
        </svg>
      </div>
      <div class="image-container">
        <img src="/img/lunodog.png"/>
      </div>
    </div>

    <!-- middle part -->
    <div class="middle">
      <FeatureBanner
        title="YouTube & Twitch tracking"
        description="Announce streams and new videos of your guild by members activity or a custom channels list."
        image="/img/features/streams.png"
      />
      <FeatureBanner
        title="Isolator"
        description="Trap members into custom isolation roles. Enjoy the detailed log."
        image="/img/features/durka.png"
        :odd=true
      />
      <FeatureBanner
        title="YouTube & Twitch tracking"
        description="Announce streams and new videos of your guild by members activity or a custom channels list."
        image="/img/features/streams.png"
      />
      <FeatureBanner
        title="YouTube & Twitch tracking"
        description="Announce streams and new videos of your guild by members activity or a custom channels list."
        image="/img/features/streams.png"
        :odd="true"
      />
    </div>

    <!-- bottom part -->
    <div class="bottom">
      <span>© Leshaka</span>
      <!-- twith icon -->
      <svg viewBox="0 0 32 32">
        <path d="M 2.9042969,0.64453125 0.98632812,6.2949219 1.0351562,27.849609 h 7.5097657 l 0.037109,3.761719 4.6035161,0.05078 3.78125,-3.738281 5.605469,-0.01953 8.496093,-8.423828 -0.0039,-18.77539088 z M 28.341797,3.4238281 28.330078,18.564453 23.585938,23.265625 16.0625,23.238281 12.269531,26.986328 12.242188,23.216797 5.7128906,23.34375 5.6816406,3.4433594 Z m -12.318359,5.7421875 -2.8125,0.013672 0.0293,8.3457034 2.794922,0.01953 z m 4.80664,0.00391 v 8.3554694 l 2.69336,0.0039 V 9.1699219 Z"/>
      </svg>
      <!-- youtube icon -->
      <svg viewBox="0 0 32 32">
        <path d="m 5.9374352,5.0847303 c -3.2402464,0 -5.84961989,1.8568084 -5.84961989,4.161248 V 23.139549 c 0,2.30444 2.60937349,4.159356 5.84961989,4.159356 H 26.093728 c 3.240256,0 5.849629,-1.854916 5.849629,-4.159356 V 9.2459783 c 0,-2.3044396 -2.609373,-4.161248 -5.849629,-4.161248 z m 6.7307658,6.0770157 8.457043,4.763839 -8.273229,4.930588 z"/>
      </svg>
    </div>

  </div>
</template>

<script>
import FeatureBanner from '@/components/FeatureBanner.vue'

export default {
  components: { FeatureBanner },
  inject: ["$oauthURI", "$staticPath"]
}
</script>

<style lang="scss" scoped>

  .layout {
    display: flex;
    flex-direction: column;

    min-width: 100%;
    min-height: 100vh;
  }

  // Upper banner

  .upper {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 400px;
    background-color: var(--bgc1);

    * {
      z-index: 1;
    }

    .waves-container {
      display: flex;
      flex-direction: row;
      align-items: flex-end;
      position: absolute;
      width: 100%;
      height: 400px;
      z-index: 0;

      path {
        fill: var(--bgc0);
      }
    }

    .image-container {
      display: flex;
      flex-direction: row;
      align-items: flex-end;
      justify-content: flex-end;

      position: absolute;
      width: 100%;
      height: 400px;
      z-index: 0;
    }

    .menu {
      color: var(--font-bright);
      font-family: roboto-light;
      padding-top: 10px;
      a {
        margin: 0 10px 0 10px;
        border-color: var(--font-bright);
        cursor: pointer;
      }
      a:hover {
        border-bottom: 1px solid;
      }
    }

    .title {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      font-family: holtwood;
      font-size: 48px;
      color: var(--font-bright);
      flex: 1 1 auto;
      .description {
        font-family: roboto-light;
        font-size: 18px;
      }
    }

    .button { // discord login button, should not use variable colors
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
    
      background: #5865f2;
      padding: 10px 30px 10px 30px;
      margin-bottom: 20px;
      border-radius: 20px;
      cursor: pointer;
      span {
        color: white;
        font-family: roboto;
        font-size: 18px;
        margin-right: 10px;
      }
    }

    .button:hover {
      filter: brightness(120%);
    }
  }

  // Middle area with features list

  .middle {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    align-content: stretch;

    flex: 1 1 auto;
  }

  // Bottom footer

  .bottom {
    display: flex;
    flex-direction: row;
    align-items: center;
    height: 42px;
    background-color: var(--bgc1);
    border-top: 12px var(--bgc-bright2) solid;
    padding-left: 10px;

    span {
      color: var(--font-normal);
      font-family: roboto-light;
      font-size: 14px;
    }

    svg {
      height: 18px;
      width: 18px;
      margin-left: 5px;
      cursor: pointer;
    }

    path {
      fill: var(--font-dimm);
    }

    svg:hover path {
      fill: var(--font-bright);
    }
  }
</style>