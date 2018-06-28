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
//import 'vue-material/dist/theme/default.css'
import axios from 'axios'
import VueAxios from 'vue-axios';
import VueAuth from '@websanova/vue-auth'
import authHeader from './components/authHeader'

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
    this.$user.logout()
    router.push({name: 'Login', params: {prev_url: prev}});
  }
}

/* Function that adds the bearer jwt to the header.
   This cannot be done via vue-auth, because of our
   custom $ajax wrapper.
*/
function add_bearer(hdr) {
    let token = window.$auth.token();
    if (token) {
        hdr['Authorization'] = 'Bearer ' + token;
    }
    return hdr;
}

//Vue.prototype.$user = null
Vue.prototype.$ajax = {
    get: function (url, data, f) {
        let hdr = {};

        if (typeof data == 'function') {
            f = data
            data = {}
        }

        hdr = add_bearer(hdr);

        let axios_auth = axios.create({
            headers: hdr
        });
        return axios_auth.get(url, data).then(f).catch(handle_ajax_error);
    },
  post: function (url, data={}, f) {
    let hdr = {};

    hdr = add_bearer(hdr);

    hdr['X-CSRFToken'] = csrf_token;
    let axios_csrf = axios.create({
      headers: hdr
    });
      return axios_csrf.post(url, data).then(f).catch(handle_ajax_error);
  },
  delete: function (url, data={}, f) {
    let hdr = {};

    hdr = add_bearer(hdr);

    hdr['X-CSRFToken'] = csrf_token;
    let axios_csrf = axios.create({
      headers: hdr
    });
      return axios_csrf.delete(url, data).then(f).catch(handle_ajax_error);
  },
  put: function (url, data={}, f) {
    let hdr = {};

    hdr = add_bearer(hdr);

    hdr['X-CSRFToken'] = csrf_token;
    let axios_csrf = axios.create({
      headers: hdr
    });
      return axios_csrf.put(url, data).then(f).catch(handle_ajax_error);
  },
  patch: function (url, data={}, f) {
    let hdr = {};

    hdr = add_bearer(hdr);

    hdr['X-CSRFToken'] = csrf_token;
    let axios_csrf = axios.create({
      headers: hdr
    });
    return axios_csrf.patch(url, data).then(f).catch(handle_ajax_error)
  },
}

Vue.prototype.$user = {
  get: function () {
    let usr = $auth.user();
    return usr;
  },

  set: function (user) {
    return $auth.user(user);
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

  logged_in: function () {
    return $auth.check()
  },

  isStudent: function () {
    return $auth.check('student');
  },

  isSupervisor: function () {
    return $auth.check('supervisor');
  },

  isTa: function () {
    return $auth.check('ta');
  }
}

Vue.prototype.$lti = {
    data: {
        lti_session: false,
        lti_data: {}
    },
};

Vue.axios = axios
Vue.router = router

Vue.use(VueAuth, {
  auth: authHeader,
  http: require('@websanova/vue-auth/drivers/http/axios.1.x.js'),
  router: require('@websanova/vue-auth/drivers/router/vue-router.2.x.js'),
  token: [
    {request: 'access_token', response: 'access_token', authType: 'Bearer', foundIn: 'header'},
    {request: 'Authorization', response: 'Authorization', authType: 'Bearer', foundIn: 'header'},
  ],
  fetchData: {url: '/api/user/retrieve', method: 'GET', enabled: true},
  refreshData: {url: '/api/user/retrieve', method: 'GET', enabled: true},
  loginData: {url: '/api/login', fetchUser: true},
  tokenDefaultName: 'access_token',
    parseUserData: function (data) {
        if (data.json_data)
            return data.json_data.user
        return data.json_data
  },
  tokenStore: ['localStorage', 'cookie']
});


window.$auth = Vue.auth;
window.Auth = VueAuth;
window.$user = Vue.prototype.$user;
window.$current_course_id = null;
window.$rederict_to_ticket = null;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
})
