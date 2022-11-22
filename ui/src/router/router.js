import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '@/pages/MainPage'
import ErrorPage from '@/pages/ErrorPage'
import LoginPage from '@/pages/LoginPage'
import Oauth2Page from '@/pages/Oauth2Page'



const routes = [
  {
    name: 'mainPage',
    path: '/:module?',
    component: MainPage,
    props: true
  },
  {
    name: 'errorPage',
    path: '/error',
    component: ErrorPage,
    props: true
  },
  {
    name: 'loginPage',
    path: '/login',
    component: LoginPage,
    props: true
  },
  {
    name: 'oauth2Page',
    path: '/oauth',
    component: Oauth2Page
  }
]

const router = createRouter({
  routes,
  history: createWebHistory(process.env.BASE_URL)
})

export default router;