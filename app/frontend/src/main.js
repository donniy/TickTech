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
import axios from 'axios'
import VueCookies from 'vue-cookies'

Vue.use(VeeValidate);
Vue.config.productionTip = false
Vue.use(BootstrapVue)
Vue.use(VueSocketio, 'http://' + document.domain + ':' + location.port)
Vue.use(VueTextareaAutosize)
Vue.use(VueGridLayout)

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './assets/scss/style.scss'

function handle_ajax_error(error) {
  console.warn(error);
  if (error.response.status === 401) {
    console.warn("Not authorized!");
    let prev = '/';
    console.log(router.currentRoute.fullPath);
    if(router.currentRoute.fullPath !== '/login')
      prev = router.currentRoute.fullPath;
    else if (typeof router.params !== 'undefined' && typeof router.params.prev_url !== 'undefined')
      prev = router.params.prev_url;
    router.push({name: 'Login', params: {prev_url: prev}});
  }
}

//Vue.prototype.$user = null
Vue.prototype.$ajax = {
  get: function (url, f) {
    let hdr = {};

    let token = window.$cookies.get('token')

    if(token)
      hdr['Authorization'] = 'JWT ' + token;

    let axios_auth = axios.create({
      headers: hdr
    });
    return axios_auth.get(url).then(f).catch(handle_ajax_error)
  },
  post: function (url, data={}, f) {
    let hdr = {};

    let token = window.$cookies.get('token')

    if(token)
      hdr['Authorization'] = 'JWT ' + token;

    hdr['X-CSRFToken'] = csrf_token;
    let axios_csrf = axios.create({
      headers: hdr
    });
    return axios_csrf.post(url, data).then(f).catch(handle_ajax_error)
  }
}

Vue.prototype.$user = {
  get: () => {
    let user_json = window.$cookies.get('user');

    let user_obj = null;

    try {
      user_obj = JSON.parse(user_json);
    } catch(e) {
      return null;
    }

    return user_obj;
  },

  set: (user) => {
    if (typeof user === 'undefined')
      return false;

    let user_json = null;
    try {
      user_json = JSON.stringify(user);
      window.$cookies.set('user', user_json);
    } catch(e) {
      return false;
    }

    return true;
  }
}

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
