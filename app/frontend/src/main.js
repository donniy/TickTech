// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App'
import VeeValidate from 'vee-validate';
import VueSocketio from 'vue-socket.io';
import VueTextareaAutosize from 'vue-textarea-autosize'
import router from './router'
import VueGridLayout from 'vue-grid-layout'

Vue.use(VeeValidate);
Vue.config.productionTip = false
Vue.use(BootstrapVue)
Vue.use(VueSocketio, 'http://' + document.domain + ':' + location.port)
Vue.use(VueTextareaAutosize)
Vue.use(VueGridLayout)

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './assets/scss/style.scss'

Vue.prototype.$user = null

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
