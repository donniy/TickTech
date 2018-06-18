<template>
    <div>
        <button class="btn btn-primary back-button" v-on:click="goCourse('/course/' + ticket.course_id)">
            Terug naar cursus
        </button>

        <button class="btn btn-primary close-button" @click="showModal = true">
            Close Ticket
        </button>

        <modal v-if="showModal" warning="Are you sure you want to close this ticket?" @yes="closeTicket()" @close="showModal = false"></modal>
        <br />
        <br />

        <div class="row">
            <div class="col-md-8 col-sm-8 col-lg-8 col-xs-12">
                <h2>Ticket Info</h2>
                <div class="material-card">
                    <div>
                        <h2>{{ticket.title}}</h2>
                        Status: {{ticket.status.name}}
                    </div>
                    <div>
                        Ta's:
                        <b v-for="ta in ticket.tas" v-bind:key="ta.id" v-bind:ta="ta">
                            {{ ta.name}}
                        </b>
                    </div>
                </div>

                <message v-bind:user="{id: user_id}" v-for="message in messages" v-bind:key="message.id" v-bind:message="message"></message>

                <form v-on:submit.prevent="sendReply" class="reply-area">
                    <h4>Respond</h4>
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
                <b-popover ref="popoverRef" target="popoverButton-sync" triggers="click blur" placement='top'>
                    <vue-tribute :options="mentionOptions" v-on:tribute-replaced="matchFound">
                        <textarea v-model="noteTextArea" class="form-control" id="textAreaForNotes" style="height:200px;width:250px;" placeholder="Voer uw opmerking in">

                        </textarea>
                    </vue-tribute>
                    <button @click="addNote" class="btn btn-primary" style="margin-top:10px">Verzenden</button>
                </b-popover>
            </div>
        </div>
    </div>
</template>

<script>

    import Message from './Message.vue'
    import VueTribute from 'vue-tribute'
    import Modal from './ClosePrompt.vue'
    import Note from './Note.vue'


    /* This is an addition to the default config
     * for tributejs.
     * DOCS: https://github.com/zurb/tribute
     */
    let defaultMention = {
        values: [
        ],

        selectTemplate: function (item) {
            return '@' + item.original.id
        },
        lookup: function (ta) {
            return ta.name + ' ' + ta.id
        }
    }


    export default {
        data() {
            return {
                showModal: false,
                user_id: 0,
                ticket: {
                    title: '',
                    status: {
                        name: ''
                    },
                    course_id: '',
                    tas: []
                },
                reply: '',
                messages: [],
                notes: [],
                show: false,
                noteTextArea: "",
                course_tas: [],
                mentionOptions: defaultMention,
            }
        },
        methods: {
            goCourse(here) {
                this.$router.push(here)
            },
            getTicket() {
                const path = '/api/ticket/' + this.$route.params.ticket_id
                this.$ajax.get(path)
                    .then(response => {
                        this.ticket = response.data.json_data
                        this.getCourseTas()
                    }).catch(error => {
                        console.log(error)
                    })
            },
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
            getNotes() {
                //get all notes
                this.$ajax.get('/api/notes/' + this.$route.params.ticket_id)
                    .then(response => {
                        this.notes = response.data.json_data
                        console.log(response)
                    })
                    .catch(err => {
                        console.log(err)
                    })
            },
            sendReply() {
                const path = '/api/ticket/' + this.$route.params.ticket_id + '/messages'
                this.$ajax.post(path, {
                    message: this.reply,
                    user_id: this.user_id
                })
                    .then(response => {
                        this.reply = ''
                        this.getMessages()
                    })
                    .catch(error => {
                        console.log(error)
                    })
            },
            closeTicket() {
                this.showModal = false
                const path = '/api/ticket/' + this.$route.params.ticket_id + '/close'
                this.$ajax.post(path)
                    .then(response => {
                        // TODO: Iets van een notificatie ofzo? '234 closed this ticket'? iig niet meer hardcoden "closed"
                        this.ticket.status.name = "closed"
                    })
            },
            addNote() {
                console.log(this.noteTextArea)
                const path = '/api/notes'
                var noteData = {
                    "ticket_id": this.$route.params.ticket_id,
                    "user_id": this.$route.params.user_id | 1,
                    "text": this.noteTextArea
                }
                console.log("Note")
                console.log(this.noteTextArea)
                this.$ajax.post(path, noteData)
                    .then(response => {
                        this.noteTextArea = ""
                        this.$refs.popoverRef.$emit('close')
                        this.notes.push(response.data.json_data)
                    })
                    .catch(error => {
                        console.log(error)
                    })
            },

            /* Get the ta's in this course. Will add all the ta's to the
             * course_tas array.
             * NOTE: This can maybe stay local and course_tas can be removed from data.
             */
            getCourseTas() {
                const path = '/api/courses/' + this.ticket.course_id + '/tas'
                this.$ajax.get(path)
                    .then(response => {
                        this.course_tas = response.data.json_data
                        build_ta_matching_table(this)
                    }).catch(error => {
                        console.log(error)
                    })

                /* Function to build the matching table for mentioning.
                 * It grabs all ta's for this course and appends them to the
                 * table.
                 */
                function build_ta_matching_table(obj) {
                    console.log(obj.mentionOptions)
                    // Vue-tribute keeps an instance of the Optionsarray, so clear it.
                    // Yes this is a valid way to clear out an array in JS.
                    obj.mentionOptions.values.length = 0;
                    for (let i = 0; i < obj.course_tas.length; i++) {
                        let ta = obj.course_tas[i]
                        console.log(ta)
                        obj.mentionOptions.values.push(
                            { name: String(ta.name), id: String(ta.id) })
                    }
                }
            },

            /* This replaced the noteTextArea when a match if found. Otherwise
               The user has to append a space after matching to include the whole match.
               So this makes it possible to click on a match and then immediately post
               The note.
             */
            matchFound(e) {
                let matchedValue = document.getElementById("textAreaForNotes").value
                this.noteTextArea = matchedValue
            },
        },
        mounted: function () {
            if (!this.$user.logged_in()) {
                this.$router.push('/login')
            }
            this.user_id = this.$user.get().id
            this.getTicket()
            this.getMessages()
            this.getNotes()
            this.$socket.emit('join-room', { room: 'ticket-messages-' + this.$route.params.ticket_id })
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
            'modal': Modal,
            'note': Note,
            VueTribute,
        },
        watch: {
        }
    }
</script>
