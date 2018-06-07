<template>
    <div>
        <a href="/user/123123123" class="btn btn-primary back-button">&laquo; Terug naar overzicht</a>
        <br /><br />
        <h1>Mijn ticket</h1>
        <div class="material-card">
            <h2>{{ticket.title}}</h2>
            Status: {{ticket.status.name}}
        </div>

        <message v-bind:self="123123123" v-for="message in messages" v-bind:key="message.id" v-bind:message="message"></message>

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

const axios_csrf = axios.create({
  headers: {'X-CSRFToken': csrf_token}
});

export default {
    data () {
        return {
            ticket: {title: '', status: {name: ''}, course_id: ''},
            reply: '',
            messages: [],
        }
    },
    methods: {
        getTicket () {
            const path = '/api/ticket/' + this.$route.params.ticket_id
            axios.get(path)
            .then(response => {
                this.ticket = response.data
            })
            .catch(error => {
                console.log(error)
            })
        },
        getMessages () {
            const path = '/api/ticket/' + this.$route.params.ticket_id + '/messages'
            axios.get(path)
            .then(response => {
                this.messages = response.data.json_list
            })
            .catch(error => {
                console.log(error)
            })
        },
        sendReply () {
            const path = '/api/student/ticket/' + this.$route.params.ticket_id + '/reply'
            axios_csrf.post(path, {message: this.reply})
            .then(response => {
                if (response.data.status == "success") {
                    this.reply = ''
                }
            })
            .catch(error => {
                console.log(error)
            })
        }
    },
    mounted: function () {
        this.getTicket()
        this.getMessages()
        this.$socket.emit('join-room', {room: 'ticket-messages-' + this.$route.params.ticket_id})
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
    }
}

</script>
