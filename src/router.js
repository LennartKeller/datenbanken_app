import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Api from './views/Api.vue'
import TextBox from './views/TextBox.vue'
import TaskView from '@/views/TaskView'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/api',
      name: 'api',
      component: Api
    },
    {
      path: '/text',
      name: 'text',
      component: TextBox
    },
    {
      path: '/task-view',
      name: 'task-view',
      component: TaskView
    }
  ]
})
