<template>
    <div>
        <router-link :to="{path: ret_url}" class="btn btn-primary back-button">&laquo; Terug naar overzicht</router-link>
        <br /><br />
        <h1>Mijn ticket</h1>
        <div class="material-card">
            <h2>{{ticket.title}}</h2>
            Status: {{ticket.status.name}}
        </div>

        <message v-bind:user="user" v-for="message in messages" v-bind:key="message.id" v-bind:message="message"></message>

        <form v-on:submit.prevent="sendReply" class="reply-area">
            <h4>Provide additional information</h4>
            <hr />
            <textarea v-model="reply" rows="6" placeholder="Schrijf een reactie..."></textarea>
            <button class="btn btn-primary">Submit reaction</button>
        </form>
    </div>
</template>

<script>
    import Message from './Message.vue'
    import VueCookies from 'vue-cookies'


export default {
    data () {
        return {
            ticket: {title: '', status: {name: ''}, course_id: ''},
            reply: '',
            messages: [],
            ret_url: '',
            user: null //window.$user.get()
        }
    },
    methods: {
        getTicket () {
            const path = '/api/ticket/' + this.$route.params.ticket_id
            this.$ajax.get(path)
            .then(response => {
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
            console.log(this.user);
            this.$ajax.post(path, {message: this.reply, user_id:this.user})
            .then(response => {
                    this.reply = ''
            })
            .catch(error => {
                console.log(error)
            })
        }
    },
    mounted: function () {
        this.user = this.$user.get().id;
        this.ret_url = '/user/' + this.user;
        console.log("id: " + this.user);
        console.log(this.ret_url)
        this.getTicket();
        this.getMessages();
        this.$socket.emit('join-room', {room: 'ticket-messages-' + this.$route.params.ticket_id});
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
