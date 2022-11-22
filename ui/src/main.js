import { cfg } from './config'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App'
import router from './router/router'
import './assets/css/themes.scss'


const pinia = createPinia()
const app = createApp(App)

app.provide('$oauthURI', cfg.oauthURI)
app.provide('$staticPath', cfg.staticPath)
app.provide('$apiURL', cfg.apiURL)


app.use(pinia)
app.use(router)
app.mount('#app')
