import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '@/pages/MainPage'
import ErrorPage from '@/pages/ErrorPage'
import SettingsPage from '@/pages/SettingsPage'
import Oauth2Page from '@/pages/Oauth2Page'



const routes = [
  {
    name: 'mainPage',
    path: '/',
    component: MainPage
  },
  {
    name: 'errorPage',
    path: '/error',
    component: ErrorPage
  },
  {
    name: 'oauth2Page',
    path: '/oauth',
    component: Oauth2Page
  },
  {
    name: 'settingsPage',
    path: '/login',
    component: SettingsPage
  },

]

const router = createRouter({
  routes,
  history: createWebHistory(process.env.BASE_URL)
})

export default router;