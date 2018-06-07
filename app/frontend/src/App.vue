<template>
    <div id="app">
        <navbar v-bind:active="active"></navbar>
        <div class="navbar-spacing"></div>
        <div class="container">
        <router-view v-on:tab-activate="active = arguments[0]"/>
        </div>
    </div>
</template>

<script>

import Navbar from './components/Navbar.vue'

export default {
    name: 'App',
    data () {
      return {
        active: 'home'
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

