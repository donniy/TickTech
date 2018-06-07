<template>
    <div>
        <a v-bind:href="'/course/' + ticket.course_id" class="btn btn-primary back-button">&laquo; Terug naar cursus</a>
        <button class="btn btn-primary close-button" @click="showModal = true">Close Ticket</button>
        <modal  v-if="showModal" @yes="closeTicket()" @close="showModal = false">
        </modal>
        <br /><br />
        <div class="row">
            <div class="col-md-8 col-sm-8 col-lg-8 col-xs-12">
                <h2>Ticket Info</h2>
                <div class="material-card">
                    <h2>{{ticket.title}}</h2>
                    Status: {{ticket.status.name}}
                </div>

                <message v-bind:self="12345678" v-for="message in messages" v-bind:key="message.id" v-bind:message="message"></message>

                <form v-on:submit.prevent="sendReply" class="reply-area container">
                    <textarea v-model="reply" placeholder="Schrijf een reactie..."></textarea>
                    <button class="reply-button btn btn-primary">
                        <i class="material-icons">
                            send
                        </i>
                    </button>
                </form>
            </div>
            <div class="col-md-4 col-sm-4 col-lg-4 col-xs-12">
                <h2>Notities</h2>
                <note v-for="note in notes" v-bind:key="note.id" v-bind:note="note"></note>

                <b-btn id="popoverButton-sync" variant="primary" class="note-add-button btn btn-primary">
                    Notitie toevoegen
                </b-btn>

                <b-popover ref="popoverRef" target="popoverButton-sync" 
                           triggers="click blur"
                           placement='top'>
                    <textarea v-model="noteTextArea" class="form-control" style="height:200px;width:250px;" 
                            placeholder="Voer uw opmerking in"></textarea>
                    <button @click="addNote" class="btn btn-primary" style="margin-top:10px">Verzenden</button>
                </b-popover>
            </div>
        </div>
    </div>
</template>

<script>

import axios from 'axios'
import Message from './Message.vue'

import Modal from './ClosePrompt.vue'
import Note from './Note.vue'

const axios_csrf = axios.create({
  headers: {'X-CSRFToken': csrf_token}
});

export default {
    data () {
        return {
            showModal: false,
            ticket: {title: '', status: {name: ''}, course_id: ''},
            reply: '',
            messages: [],
            notes: [],
            show: false,
            noteTextArea: ""
        }
    },
    methods: {
        getTicket () {
            const path = '/api/ticket/' + this.$route.params.ticket_id
            axios.get(path)
            .then(response => {
                this.ticket = response.data

                //get all notes
                axios.get('/api/notes/'+this.$route.params.ticket_id)
                .then(res => {
                    this.notes = res.data
                    console.log(res)
                })
                .catch(err => {
                    console.log(err)
                })
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
                    this.reply = ''
                }
            })
            .catch(error => {
                console.log(error)
            })
        },
        closeTicket () {
            this.showModal = false
            const path = '/api/ticket/' + this.$route.params.ticket_id + '/close'
            axios_csrf.post(path)
            .then(response => {
                // TODO: Iets van een notificatie ofzo? '234 closed this ticket'?
            })
        },
        addNote(){
            console.log(this.noteTextArea)
            const path = '/api/note/add'
            var noteData = {
                "ticket_id":this.$route.params.ticket_id ,
                "user_id":this.$route.params.user_id ,
                "message":this.noteTextArea
            }

            axios_csrf.post(path, noteData)
            .then(response => {
                this.noteTextArea = ""
                this.$refs.popoverRef.$emit('close')
                console.log("successfully sent note")
                console.log(response)
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
    sockets: {
        connect: function () {
        },
        messageAdded: function (data) {
            console.log(data)
            this.messages.push(data)
        }
    },
    components: {
        'message': Message,
        'modal' : Modal,
        'note': Note
    }
}

</script>
