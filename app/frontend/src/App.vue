<template>
    <div id="app">
        <navbar v-bind:active="active"></navbar>
        <!-- <div class="navbar-spacing"></div> -->
        <div v-if="isHome" class="container-fluid first-background-image">
            <router-view />
        </div>
        <div v-else="isHome" class="container">
            <router-view />
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
        isHome: false
      }
    },
    watch:{
        $route (to, from) {
            console.log(to.name)
            if(to.name === 'Home') {
                this.isHome = true
            } else {
                this.isHome = false
            }
        }
    },
    components: {
        'navbar': Navbar,
    },
}

</script>

<style scoped>
li a:hover {
    background-color: #fff;
}

li {
    height:100%;
}
.active {
    background-color: #fff;
}

ul {
    padding: 0;
    margin: 0;
}

nav {
    padding: 0;
}
li a {
    color: white;
    text-align: center;
    text-decoration: none;
}

nav {
    height: 100%;
}
</style>
