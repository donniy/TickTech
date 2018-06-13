<template>
    <div>
        <router-link to="/user/123123123" class="btn btn-primary back-button">&laquo; Terug naar overzicht</router-link>
        <br /><br />
        <h1>Mijn ticket</h1>
        <div class="material-card">
            <div>
                <h2>{{ticket.title}}</h2>
                Status: {{ticket.status.name}}
            </div>
            <div>
                Ta's:
                <b v-for="user in ticket.tas" v-bind:key="user.id" v-bind:user="user">
                    {{ user.name}} 
                </b>
            </div>
        </div>

        <message v-bind:user="user" v-for="message in messages" v-bind:key="message.id" v-bind:message="message"></message>

        <form v-on:submit.prevent="sendReply" class="reply-area">
            <textarea v-model="reply" placeholder="Schrijf een reactie..."></textarea>
            <button class="reply-button btn btn-primary">
                <i class="material-icons">
                    send
                </i>
            </button>
        </form>
    </div>
</template>

<script>

import axios from 'axios'
import Message from './Message.vue'
import VueCookies from 'vue-cookies'

export default {
    data () {
        return {
            ticket: {title: '', status: {name: ''}, course_id: '', tas:[]},
            reply: '',
            messages: [],
            user: {}
        }
    },
    methods: {
        getTicket () {
            const path = '/api/ticket/' + this.$route.params.ticket_id
            this.$ajax.get(path)
            .then(response => {
                console.log(response)
                this.ticket = response.data.json_data
            })
            .catch(error => {
                console.log(error)
            })
        },
        getMessages () {
            const path = '/api/ticket/' + this.$route.params.ticket_id + '/messages'
            this.$ajax.get(path)
            .then(response => {
                this.messages = response.data.json_data
            })
            .catch(error => {
                console.log(error)
            })
        },
        sendReply () {
            const path = '/api/ticket/' + this.$route.params.ticket_id + '/messages'
            this.$ajax.post(path, {message: this.reply, user_id:4321})
            .then(response => {
                    this.reply = ''
            })
            .catch(error => {
                console.log(error)
            })
        }
    },
    mounted: function () {
        this.user = this.$user.get()
        console.log(this.user)
        console.log("id: " + this.user.id)
        this.getTicket()
        this.getMessages()
        this.$socket.emit('join-room', {room: 'ticket-messages-' + this.$route.params.ticket_id})
    },
    beforeRouteLeave: function (to, from, next) {
        this.$socket.emit('leave-room', {room: 'ticket-messages-' + this.$route.params.ticket_id})
        next();
    },
    components: {
        'message': Message,
    },
    sockets: {
        connect: function () {
            console.log("Socket connection!")
        },
        messageAdded: function (data) {
            console.log(data)
            this.messages.push(data)
            document.body.scrollTop = document.body.scrollHeight;
        }
    },
}

</script>
