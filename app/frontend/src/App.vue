<template>
    <div id="app">
        <navbar v-bind:transparent="navbarTransparent" v-bind:active="active"></navbar>
        <div v-if="isHome" class="container-fluid">
            <router-view />
        </div>
        <div v-else class="container-fluid second-background-image">
            <div class="navbar-spacing"></div>
            <div class="container">
                <router-view />
            </div>
        </div>
        <md-snackbar md-position="left" :md-active.sync="showSnackbar" md-persistent>
            <span>{{ snackbar.text }}</span>
            <md-button class="md-primary" @click="$router.push('/ticket/' + snackbar.ticket)">OPEN</md-button>
        </md-snackbar>
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
            navbarTransparent: true,
            snackbar: {
                text: "snackbar test",
                ticket: ""
            },
            showSnackbar: false,
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
    sockets: {
        connect: function () {
            console.log("Socket connected")
            if (this.$user.logged_in()) {
                this.$socket.emit('join-room', {room: 'user-' + this.$user.get().id})
            } else {
                console.log("not logged in")
            }
        },
        'message': function (data) {
            console.log("received message")
            console.log(data)
            let text = ""
            switch (data.type) {
                case 0:
                    text = data.sender.name + ' responed to "' + data.ticket_title + '": ' + data.text
                    break;
                case 1:
                    // Status changed
                    break;
                case 2:
                    // Ticket closed
                    text = data.sender.name + ' closed "' + data.ticket_title + '"'
                    break;
                case 3:
                    // New ticket
                    text = 'New ticket: ' + data.ticket_title
                    break;
            }
            this.snackbar.text = text
            this.snackbar.ticket = data.ticket
            this.showSnackbar = true
        },
        'join-room': function (data) {
            console.log("Join room:")
            console.log(data)
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
