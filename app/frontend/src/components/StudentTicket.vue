<!-- StudentTicket.vue shows a ticket from the student perspective. -->
<template>
    <div>
        <router-link :to="{path: ret_url}" class="btn btn-primary back-button">&laquo; Back to overview </router-link>
        <router-link :to="{path: ret_url}" class="btn btn-primary">&laquo; Back home</router-link>
        </md-button>

        <br />
        <br />
        <h1>My ticket</h1>
        <div class="material-card">
            <h2>{{ticket.title}}</h2>
            Status: {{ticket.status.name}}
            </br>
            <div class="file-name-container-small medium-12 small-12 cell" v-if="ticket.files.length > 0">
                <div v-for="file in ticket.files">
                    <p v-on:click="downloadFile(file.file_location, file.file_name)" class="file-listing-small">
                        <i class="material-icons download-icon">folder</i> {{ file.file_name }}</p>
                </div>
            </div>
        </div>

        <message v-bind:user="user" v-for="message in messages" v-bind:key="message.id" v-bind:message="message"></message>

        <form v-on:submit.prevent="sendReply" class="reply-area">
            <h4>Provide additional information</h4>
            <textarea v-model="reply" rows="6" placeholder="Write a reply..."></textarea>
            <button style="margin-bottom:10px;" class="btn btn-primary">Submit reply</button>
        </form>
        <form class="hidden-input" action="/api/ticket/filedownload" method="POST">
            <input type="hidden" name="file" value="value1">...</form>
    </div>
</template>

<script>
    import Message from './Message.vue'
    import VueCookies from 'vue-cookies'


    export default {
        data() {
            return {
                ticket: { title: '', status: { name: '' }, course_id: '', files: [] },
                reply: '',
                messages: [],
                ret_url: '',
                user: this.$user.get()
            }
        },
        methods: {
            // Retrieve a ticket.
            getTicket() {
                const path = '/api/ticket/' + this.$route.params.ticket_id
                this.$ajax.get(path)
                    .then(response => {
                        this.ticket = response.data.json_data
                    })
                    .catch(error => {
                        console.log(error)
                    })
            },
            // Retrieve the replies. 
            getMessages() {
                const path = '/api/ticket/' + this.$route.params.ticket_id + '/messages'
                this.$ajax.get(path)
                    .then(response => {
                        this.messages = response.data.json_data
                    })
                    .catch(error => {
                        console.log(error)
                    })
            },
            // Sent a reply.
            sendReply() {
                const path = '/api/ticket/' + this.$route.params.ticket_id + '/messages'
                console.log(this.user)
                this.$ajax.post(path, { message: this.reply, user_id: this.user })
                    .then(response => {
                        this.reply = ''
                    })
                    .catch(error => {
                        console.log(error)
                    })
            },
            // Creates a Blob object
            b64toBlob(b64Data, contentType, sliceSize) {
                contentType = contentType || ''
                sliceSize = sliceSize || 512

                var byteCharacters = atob(b64Data)
                console.log(byteCharacters)

                var byteArrays = []

                for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
                    var slice = byteCharacters.slice(offset, offset + sliceSize)

                    var byteNumbers = new Array(slice.length)
                    for (var i = 0; i < slice.length; i++) {
                        byteNumbers[i] = slice.charCodeAt(i)
                    }

                    var byteArray = new Uint8Array(byteNumbers)

                    byteArrays.push(byteArray)
                }

                var blob = new Blob(byteArrays, { type: contentType })
                return blob
            },
            // Download the submitted files.
            downloadFile(key, name) {
                const path = '/api/ticket/filedownload'
                this.$ajax.post(path, { address: key })
                    .then((response) => {
                        // Get data from response
                        var byteCharacters = atob(response.data.json_data['encstring'])
                        var mimetype = response.data.json_data['mimetype']

                        // Convert data to bytearray and decode
                        var byteNumbers = new Array(byteCharacters.length)
                        for (var i = 0; i < byteCharacters.length; i++) {
                            byteNumbers[i] = byteCharacters.charCodeAt(i)
                        }
                        var byteArray = new Uint8Array(byteNumbers)

                        // Generate blob and download element.
                        var blob = new Blob([byteArray], { mimetype })
                        const url = window.URL.createObjectURL(blob)
                        const link = document.createElement('a')

                        // Ref to the link and activate download.
                        link.href = url
                        link.setAttribute('download', name)
                        document.body.appendChild(link)
                        link.click()
                        document.body.removeChild(link)
                    })
                    .catch(error => {
                        console.log(error)
                        window.alert("File not found")
                    })
            }
        },
        // Call this function when the page is loaded.
        mounted: function () {
            if (!this.$user.logged_in()) {
                this.$router.push('/login')
            }
            this.user = this.$user.get()
            this.ret_url = '/home'
            this.getTicket()
            this.getMessages()
            this.$socket.emit('join-room', { room: 'ticket-messages-' + this.$route.params.ticket_id })
        },
        beforeRouteLeave: function (to, from, next) {
            this.$socket.emit('leave-room', { room: 'ticket-messages-' + this.$route.params.ticket_id })
            next()
        },
        components: {
            'message': Message,
        },
        sockets: {
            connect: function () {
                console.log("Socket connection!")
            },
            messageAdded: function (data) {
                console.log("Message added!")
                console.log(data)
                this.messages.push(data)
                document.body.scrollTop = document.body.scrollHeight
            }
        },
    }

</script>
