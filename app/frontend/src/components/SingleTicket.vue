<template>
<div v-if="$auth.ready()">
	<div id="loading-icon" class="loading">
		<md-progress-spinner class="md-accent" md-mode="indeterminate"></md-progress-spinner>
	</div>
	<div class="md-layout md-gutter">

		<div class="md-layout-item md-size-70 md-small-size-60">
			<div class="md-gutter">
				<div v-if="$auth.check('ta') || $auth.check('supervisor')" class="md-size-20">
					<router-link :to="'/course/' + ticket.course_id " class="btn btn-primary">&laquo; Back to course</router-link>
				</div>
                <div v-else class="md-size-20">
                    <div @click="$router.go(-1)" class="btn btn-primary">&laquo; Back</div>
                </div>
				<div class="md-size-80 center-display">
					<h3 class="">Ticket info</h3>
				</div>
			</div>

            <md-dialog :md-active.sync="showModal">
            <md-dialog-title>Do you want to close this ticket?</md-dialog-title>
            <md-dialog-actions>
                <md-button class="md-primary" @click="showModal = false">No I don't</md-button>
                <md-button class="md-primary" @click="closeTicket()">Yes, close it!</md-button>
            </md-dialog-actions>
            </md-dialog>
			<md-card class="md-layout">
				<md-card-content class="md-layout-item md-size-100">
					<div>
			            <md-speed-dial md-event="click" class="close-button" md-direction="bottom">
			                <md-speed-dial-target>
			                    <md-icon class="md-morph-initial">more_vert</md-icon>
			                    <md-icon class="md-morph-final">close</md-icon>
			                </md-speed-dial-target>
			                <md-speed-dial-content>
			                    <md-button class="md-icon-button md-raised md-accent" @click="showModal = true">
			                        <md-icon>lock</md-icon>
			                        <md-tooltip md-direction="left">Close ticket</md-tooltip>
			                    </md-button>
			                    <md-button class="md-icon-button md-raised md-accent" @click="">
			                        <md-icon>delete</md-icon>
			                        <md-tooltip md-direction="left">Delete ticket</md-tooltip>
			                    </md-button>
			                </md-speed-dial-content>
			            </md-speed-dial>
			        </div>
					<h4>Subject: {{ticket.title}}</h4>
					Response email: <b>{{ticket.email}}</b><br/>
					Status: {{ticket.status.name}}<br/>
					TAs:
					<b v-for="ta in ticket.tas" v-bind:key="ta.id" v-bind:ta="ta">
            {{ ta.name}}
        </b>
                    <b v-if="ticket.tas.length < 1">No one assigned yet</b>
                    <br/><br/> Uploaded files (Click OCR to turn photos into text):
                    <p v-show="ticket.files.length == 0">No files</p>
                    <md-card-content>
                    <div class="md-layout md-gutter" v-if="ticket.files.length > 0" v-for="file in ticket.files" v-bind:key="file.id">
                        <div class="md-size-80 md-layout-item file-listing-small" v-on:click="downloadFile(file.file_location, file.file_name)">
                            <i class="material-icons download-icon">folder</i> {{ file.file_name }}
                        </div>
                        <div v-if="file.is_ocrable"class="md-size-10 md-layout-item ocrbutton" v-on:click="downloadOcrFile(file.file_location, file.file_name)">
                            OCR
                        </div>
                    </div>
                </md-card-content>
                </md-card-content>
            </md-card>
            <md-card class="md-layout-item message-container">
                <div>
                    <md-card-content>
                        <message v-bind:user="{id: user_id}" v-for="message in messages" v-bind:key="message.id" v-bind:message="message"></message>
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
		<div class="md-layout-item md-size-30 md-small-size-40">
			<h3 class="note-title">Notes</h3>
			<note v-for="note in notes" v-bind:key="note.id" v-bind:note="note"></note>

			<md-button id="popoverButton-sync" class="center-display md-primary">
				Add a note.
			</md-button>
			<b-popover ref="popoverRef" target="popoverButton-sync" triggers="click blur" placement='top'>
				<vue-tribute :options="mentionOptions" v-on:tribute-replaced="matchFound">
					<textarea autofocus name="notefield" v-model="noteTextArea" class="form-control" id="textAreaForNotes" style="height:200px;width:250px;" placeholder="Enter a comment"></textarea>
				</vue-tribute>
				<button @click="addNote" class="btn btn-primary" style="margin-top:10px">Send</button>
			</b-popover>

            <md-content class="md-elevation-2 plugin-container" v-bind:key="plugin.id" v-for="(data, plugin) in plugins">
                <md-card-header>
                    <div class="md-title">
                        {{plugin}}
                    </div>
                </md-card-header>
                <md-list>
                    <template v-for="(value, key) in data">
                <md-subheader>
                    {{key}}
                </md-subheader>
                <md-list-item v-if="value.type === 'url'" target="__blank" :href="value.value">
                    {{value.value}}
                </md-list-item>
                <div style="padding: 4px 16px; display: inline-block" v-else-if="value.type === 'text'">
                    {{value.value}}
                </div>
                <md-list-item v-else-if="value.type === 'grade'">
                    <md-badge class="md-avatar-icon md-primary" :md-content="value.value" />
                </md-list-item>

                <md-list-item v-else>
                    {{value.value}}
                </md-list-item>
            </template>
                        <md-divider v-if="index != Object.keys(plugins).length - 1" />
				</md-list>
			</md-content>
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
                tas: [],
                files: []
            },
            reply: '',
            messages: [],
            notes: [],
            plugins: [],
            show: false,
            noteTextArea: "",
            course_tas: [],
            mentionOptions: defaultMention,
        }
    },
    methods: {
        /*
         * Get all information from a specific ticket.
         */
        getTicket() {
            const path = '/api/ticket/' + this.$route.params.ticket_id
            this.$ajax.get(path)
                .then(response => {
                    this.ticket = response.data.json_data
                    this.getCourseTas()
                }).catch(error => {
                    console.log(error)
                    this.$router.go(-1)
                })
        },
        /*
         * Get all plugins attached to the ticket.
         */
        getPlugins() {
            const path = '/api/ticket/' + this.$route.params.ticket_id + '/plugins'
            this.$ajax.get(path, response => {
                this.plugins = response.data.json_data
            })
        },
        /*
         * Load all messages between TA and student in the ticket.
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
         * Get all notes attached to a ticket.
         */
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
        /*
         * Send reply in to the database.
         */
        sendReply() {
            const path = '/api/ticket/' + this.$route.params.ticket_id + '/messages'
            let reply = this.reply
            this.reply = ''
            if (reply.length > 0) {

                this.$ajax.post(path, {
                    message: reply,
                    user_id: this.user_id
                })
                .then(response => {
                    this.reply = ''
                    this.bind_ta_to_ticket(this.ticket.id, this.$user.get().id)
					this.getMessages()
                })
                .catch(error => {
                    console.log(error)
                })
            }
        },
        /*
         * Close the ticket if the question has been answered by a TA.
         */
        closeTicket() {
            this.showModal = false
            const path = '/api/ticket/' + this.$route.params.ticket_id + '/close'
            this.$ajax.post(path)
                .then(response => {
                    // TODO: Iets van een notificatie ofzo? '234 closed this ticket'? iig niet meer hardcoden "closed"
                    this.ticket.status.name = "Closed"
                })

        },
        /*
         * Create a downloadable link. Retrieve location from the database and create a link to download the file.
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
        },
        downloadOcrFile(key, name){

            const path = '/api/ticket/gettext'

            document.getElementById('loading-icon').style.visibility = "visible"

            this.$ajax.post(path, {address: key})
            .then((response) => {
                // Get data from response
                console.log(response.data)
                const url = window.URL.createObjectURL(new Blob([response.data.json_data]))
                const link = document.createElement('a')
                document.getElementById('loading-icon').style.visibility = "hidden"
                link.href = url
                link.setAttribute('download', name + '.txt')
                document.body.appendChild(link)
                link.click()
                document.body.removeChild(link)

            })
            .catch(error => {
                console.log(error)
                window.alert("Whoops! We were unable to read anything useful here...")
            })
        },
        /*
         * Add note to database and display it in the ticket page.
         */
        addNote() {
            if (this.noteTextArea.length > 0) {
                console.log(this.noteTextArea)
                const path = '/api/notes'
                var noteData = {
                    "ticket_id": this.$route.params.ticket_id,
                    "user_id": this.$user.get().id,
                    "text": this.noteTextArea
                }
                this.$ajax.post(path, noteData)
                    .then(response => {
                        this.noteTextArea = ""
                        this.$refs.popoverRef.$emit('close')
                        this.notes.push(response.data.json_data)
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
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
            console.log("found", e)
            this.noteTextArea = matchedValue
        },
        /*
         * If a TA is mentioned by another TA this TA is also bound to the ticket.
         */
        bind_ta_to_ticket(ticketid, taid) {
            const path = '/api/ticket/addta'
            this.$ajax.post(path, { 'ticketid': ticketid, 'taid': taid })
                .then(response => {
                    console.log("OK",response)
					if (response.status == 200) {
						this.ticket.tas.push(response.data.json_data['ta'])
						this.ticket.status.name = response.data.json_data['status']
					} else {
						this.ticket.status.name = "Receiving help"
					}
                }).catch(error => {
                    console.log(error)
                })
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
        this.getPlugins()
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
