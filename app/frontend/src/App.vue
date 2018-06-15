<template>
    <div id="app">
        <navbar v-bind:transparent="navbarTransparent" v-bind:active="active"></navbar>
        <div v-if="isHome" class="container-fluid">
            <router-view />
        </div>
        <div v-else="isHome" class="container-fluid second-background-image">
            <div class="navbar-spacing"></div>
            <div class="container">
                <router-view />
            </div>
        </div>
    </div>
</template>

<script>

import Navbar from './components/Navbar.vue'

export default {
    name: 'App',
    data () {
      return {
        active: 'home',
        isHome: false,
        navbarTransparent: true
      }
    },
    watch:{
        $route (to, from) {
            console.log(to.name)
            if(to.name === 'Home') {
                this.isHome = true
                this.handleNavbarTransparency()
            } else {
                this.isHome = false
                this.navbarTransparent = false
            }
        }
    },
    methods: {
        handleNavbarTransparency: function () {
            if (!this.isHome && this.navbarTransparent) {
                this.navbarTransparent = false
                return
            }
            if (document.body.scrollTop > 100 || window.pageYOffset > 100 || document.documentElement.scrollTop > 100) {
                this.navbarTransparent = false
            } else {
                this.navbarTransparent = true
            }
        }
    },
    components: {
        'navbar': Navbar,
    },
    created () {
        window.addEventListener('scroll', this.handleNavbarTransparency);
    },
}

</script>
