import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App'
import VeeValidate from 'vee-validate';
import VueSocketio from 'vue-socket.io';
import VueTextareaAutosize from 'vue-textarea-autosize'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './assets/scss/style.scss'
import VueCookies from 'vue-cookies'
import VueScrollTo from 'vue-scrollto'
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'
import axios from 'axios'
import VueAxios from 'vue-axios';
import VueAuth from '@websanova/vue-auth'
import JWTHeader from './components/jwtHeader'

Vue.use(VueMaterial)
Vue.use(VueAxios, axios);
Vue.use(require('vue-moment'));
Vue.use(VeeValidate);
Vue.use(VueScrollTo);
Vue.config.productionTip = false
Vue.use(BootstrapVue)
Vue.use(VueSocketio, 'http://' + document.domain + ':' + location.port)
Vue.use(VueTextareaAutosize)


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
  get: function (url, data, f) {
    let hdr = {};

    if (typeof data == 'function') {
        f = data
        data = {}
    }

    let token = window.$auth.token();

    if(token)
      hdr['Authorization'] = 'Bearer ' + token;

    let axios_auth = axios.create({
      headers: hdr
    });
    return axios_auth.get(url, data).then(f).catch(handle_ajax_error)
  },
  post: function (url, data={}, f) {
    let hdr = {};

    let token = window.$auth.token();

    if(token)
      hdr['Authorization'] = 'Bearer ' + token;

    hdr['X-CSRFToken'] = csrf_token;
    let axios_csrf = axios.create({
      headers: hdr
    });
    return axios_csrf.post(url, data).then(f).catch(handle_ajax_error)
  },
  delete: function (url, data={}, f) {
    let hdr = {};

    let token = window.$auth.token();

    if(token)
      hdr['Authorization'] = 'JWT ' + token;

    hdr['X-CSRFToken'] = csrf_token;
    let axios_csrf = axios.create({
      headers: hdr
    });
    return axios_csrf.delete(url, data).then(f).catch(handle_ajax_error)
  },
  put: function (url, data={}, f) {
    let hdr = {};

    let token = window.$auth.token();

    if(token)
      hdr['Authorization'] = 'JWT ' + token;

    hdr['X-CSRFToken'] = csrf_token;
    let axios_csrf = axios.create({
      headers: hdr
    });
    return axios_csrf.put(url, data).then(f).catch(handle_ajax_error)
  },
  patch: function (url, data={}, f) {
    let hdr = {};

    let token = window.$auth.token();

    if(token)
      hdr['Authorization'] = 'JWT ' + token;

    hdr['X-CSRFToken'] = csrf_token;
    let axios_csrf = axios.create({
      headers: hdr
    });
    return axios_csrf.put(url, data).then(f).catch(handle_ajax_error)
  },
}

Vue.prototype.$user = {
  get: () => {
    let usr = window.$auth.user().user;
    return usr;
  },

  set: (user) => {
    return window.$auth.user(user);
  },

  logout: function () {
    this.$auth.logout({
      makeRequest: false,
      success: function () {
        $auth.token(null, '');
      },
      redirect: '/',
    });
  },

  logged_in: () => {
    return window.$auth.check()
  },

  isStudent: () => {
    let usr = window.$auth.user().user;
    if(typeof usr === 'undefined')
      return 0
    return (typeof usr.student !== 'undefined') ? 1 : 0
  },

  isSupervisor: () => {
    let usr = window.$auth.user().user;
    if(typeof usr === 'undefined')
      return 0
    return (typeof usr.ta !== 'undefined') ? 1 : 0
  },

  isTa: () => {
    let usr = window.$auth.user().user;
    if(typeof usr === 'undefined')
      return 0
    return (typeof usr.ta !== 'undefined') ? 1 : 0
  }
}

Vue.axios = axios
Vue.router = router

Vue.use(VueAuth, {
    auth: JWTHeader,
    http: require('@websanova/vue-auth/drivers/http/axios.1.x.js'),
    router: require('@websanova/vue-auth/drivers/router/vue-router.2.x.js'),
    token: [
      {request: 'Authorization', response: 'Authorization', authType: 'JWT', foundIn: 'header'},
      {request: 'access_token', response: 'access_token', authType: 'JWT', foundIn: 'response'}
    ],
    fetchData: {url: '/api/user/retrieve', method: 'GET', enabled: true},
    refreshData: {url: '/api/user/retrieve', method: 'GET', enabled: true},
    tokenDefaultName: 'access_token',
    parseUserData: function (data) {
        console.log(data)
        return data.json_data
    },
    tokenStore: ['localStorage', 'cookie']
});


window.$auth = Vue.auth;
window.Auth = VueAuth;
window.$user = Vue.prototype.$user;
window.$current_course_id = null;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
})
