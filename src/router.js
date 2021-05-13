import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Api from './views/Api.vue'
import TextBox from './views/TextBox.vue'
import AnnotationView from '@/views/AnnotationView'
import CollectionList from '@/views/CollectionList'
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
      path: '/collection',
      name: 'collectionList',
      component: CollectionList
    },
    {
      path: '/annotation-view/:collectionId',
      props: true,
      name: 'annotation-view',
      component: AnnotationView
    }
  ]
})
