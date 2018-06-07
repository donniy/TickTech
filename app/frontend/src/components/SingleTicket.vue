<template>
    <div>
        <a v-bind:href="'/course/' + ticket.course_id" class="btn btn-primary back-button">&laquo; Terug naar cursus</a>
        <a v-bind:href="ticket.course_id + '/closeticket'" class="btn btn-primary close-button">Close Ticket</a>
        <br /><br />
        <h1>Ticket Info</h1>
        <div class="material-card">
            <h2>{{ticket.title}}</h2>
            Status: {{ticket.status.name}}
        </div>

        <message v-for="message in messages" v-bind:key="message.id" v-bind:message="message"></message>

        <form v-on:submit.prevent="sendReply" class="reply-area container">
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
            const path = '/api/ticket/' + this.$route.params.ticket_id + '/reply'
            axios_csrf.post(path, {message: this.reply})
            .then(response => {
                if (response.data.status == "success") {
                    this.messages.push(response.data.message)
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
    },
    components: {
        'message': Message,
    }
}

</script>
