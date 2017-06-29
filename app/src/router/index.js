import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import Index from '@/components/Index'
import Search from '@/components/Search'
import Detail from '@/components/Detail'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: Index
    },
    {
      path: '/search/:query',
      name: 'search',
      component: Search
    },
    {
      path: '/detail/:query',
      name: 'detail',
      component:Detail
    }
  ]
})
