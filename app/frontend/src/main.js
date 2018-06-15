// hoi
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
import axios from 'axios'
import VueCookies from 'vue-cookies'
import VueScrollTo from 'vue-scrollto'

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

    let token = window.$cookies.get('token')

    if(token)
      hdr['Authorization'] = 'JWT ' + token;

    let axios_auth = axios.create({
      headers: hdr
    });
    return axios_auth.get(url, data).then(f).catch(handle_ajax_error)
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
  },
  delete: function (url, data={}, f) {
    let hdr = {};

    let token = window.$cookies.get('token')

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

    let token = window.$cookies.get('token')

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

    let token = window.$cookies.get('token')

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
  },

  logout: function () {
    $cookies.remove('user');
    $cookies.remove('token');
    router.push('/');
  },

  logged_in: () => {
    return window.$cookies.isKey('user');
    if(window.$cookies.get('user') !== null)
      return 1;
    return 0;
  },

  isStudent: () => {
    if(window.$cookies.isKey('user')) {
      let usr = window.$cookies.get('user');

      return (typeof usr.student !== 'undefined') ? 1 : 0;
    } else {
      return 0;
    }
  },

  isSupervisor: () => {
    if(window.$cookies.isKey('user')) {
      let usr = JSON.parse(window.$cookies.get('user'));

      return (typeof usr.ta !== 'undefined') ? 1 : 0;
    } else {
      return 0;
    }
  },
}

window.$user = Vue.prototype.$user;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
