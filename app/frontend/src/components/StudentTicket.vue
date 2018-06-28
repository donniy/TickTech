<template>
<div class="student-ticket-wrapper md-layout md-gutter">
    <div class="md-layout-item">
        <div class="md-gutter">
            <div class="md-size-20">
                <router-link :to="{path: ret_url}" class="btn btn-primary">&laquo; Back home</router-link>
            </div>
            <div class="md-size-80 center-display">
                <h3 class="">My Ticket</h3>
            </div>
        </div>
        <md-card class="md-layout">
            <md-card-content class="md-layout-item md-size-100">
                <h4>Subject: {{ticket.title}}</h4>
                <p>Status: {{ticket.status.name}}</p>
                Uploaded files:
                <p v-show="ticket.files.length == 0">No files</p>
                <md-card v-if="ticket.files.length > 0" v-for="file in ticket.files" v-bind:key="file.id">
                    <div class="file-listing-small" style="width:100%" v-on:click="downloadFile(file.file_location, file.file_name)">
                        <i class="material-icons download-icon">folder</i> {{ file.file_name }}
                    </div>
                </md-card>
            </md-card-content>
        </md-card>
        <md-card class="md-layout-item message-container">
            <div>
                <md-card-content>
                    <message v-bind:user="{id: user.id}" v-for="message in messages" v-bind:key="message.id" v-bind:message="message"></message>
                </md-card-content>
            </div>
        </md-card>


        <md-card class="md-layout-item message-reply-container">
            <div>
                <md-card-content>
            <form v-on:submit.prevent="sendReply">
                <md-field>
                    <label>Respond</label>
                    <md-textarea name="replyfield" v-validate="'required'" v-model="reply"></md-textarea>
                </md-field>
                <button class="btn btn-primary">Submit reply</button>
            </form>
            </md-card-content>
        </div>
        </md-card>
    </div>
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
            /*
             * Get all informtion from a specific ticket.
             */
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
            /*
             * Get all messages in a ticket between the student and a TA.
             */
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
            /*
             * Send a message to the database and display it on the ticket page.
             */
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
            /*
             * Transform the B64DATA to a byte array blob.
             */
            b64toBlob(b64Data, contentType, sliceSize) {
                  contentType = contentType || '';
                  sliceSize = sliceSize || 512;

                  var byteCharacters = atob(b64Data);
                  console.log(byteCharacters)

                  var byteArrays = [];

                  for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
                      var slice = byteCharacters.slice(offset, offset + sliceSize);

                      var byteNumbers = new Array(slice.length);
                      for (var i = 0; i < slice.length; i++) {
                          byteNumbers[i] = slice.charCodeAt(i);
                      }

                      var byteArray = new Uint8Array(byteNumbers);

                      byteArrays.push(byteArray);
                  }

                  var blob = new Blob(byteArrays, {type: contentType});
                  return blob;
            },
            /*
             * Create a downloadable link with the corresponding blob.
             */
            downloadFile(key, name){

                const path = '/api/ticket/filedownload'
                this.$ajax.post(path, {address: key})
                .then((response) => {
                    // Get data from response
                    var byteCharacters = atob(response.data.json_data['encstring']);
                    var mimetype = response.data.json_data['mimetype']

                    // Convert data to bytearray and decode
                    var byteNumbers = new Array(byteCharacters.length);
                    for (var i = 0; i < byteCharacters.length; i++) {
                        byteNumbers[i] = byteCharacters.charCodeAt(i);
                    }
                    var byteArray = new Uint8Array(byteNumbers);

                    // Generate blob and download element.
                    var blob = new Blob([byteArray], {mimetype});
                    const url = window.URL.createObjectURL(blob)
                    const link = document.createElement('a')

                    // Ref to the link and activate download.
                    link.href = url
                    link.setAttribute('download', name)
                    document.body.appendChild(link)
                    link.click();
                    document.body.removeChild(link)
                })
                .catch(error => {
                    console.log(error)
                    window.alert("File not found")
                })
            }
        },
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
