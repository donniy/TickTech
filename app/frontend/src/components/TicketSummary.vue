<template>
    <transition name="modal">
        <div class="summary-container">
            <button type="button" aria-label="Close" class="btn btn-primary close-sum" @click="$emit('close')">
                <span aria-hidden="true">&times;</span>
            </button>
            <div class="summary-wrapper">

                <div class="summary-tab-original">
                    <div class="summary-header">
                        <h3>Original message</h3>
                    </div>
                    <div class="original-summary-content">
                        <message-original v-bind:user="{id: user_id}" v-bind:tas="course_tas" v-for="message in messages.slice(0,1)" v-bind:key="message.id" v-bind:message="message">
                        </message-original>
                    </div>
                </div>

                <div class="summary-tab-middle">
                    <div class="summary-header">
                        <h3>Conversation</h3>
                    </div>
                    <div class="summary-content">
                        <p class="noreply-text" v-if="this.messages.length <= 1">No messages yet</p>
                        <message v-bind:user="{id: user_id}" v-bind:tas="course_tas" v-for="message in messages.slice(1)" v-bind:key="message.id" v-bind:message="message">
                        </message>
                    </div>
                </div>

                <div class="summary-tab-notes">
                    <div class="summary-header">
                        <h3>Notes</h3>
                    </div>
                    <div class="summary-content">
                        <note v-for="note in notes" v-bind:key="note.id" v-bind:note="note">
                        </note>
                    </div>
                </div>

            </div>
        </div>
    </transition>
</template>

<script>

    import Message from './MessageSum.vue'
    import Note from './NoteSum.vue'
    import MessageOriginal from './MessageOriginalSum.vue'

    export default {
        props: {
            ticket: Object,
        },
        data() {
            return {
                messages: [],
                user_id: 0,
                notes: [],
                course_tas: [],
            }
        },
        methods: {
            /*
             * Get all messages in a ticket between a student and a TA.
             */
            getMessages() {
                const path = '/api/ticket/' + this.ticket.id + '/messages'
                this.$ajax.get(path)
                    .then(response => {
                        this.messages = response.data.json_data
                        console.log(this.messages)
                        this.messages = this.messages.filter(el=>el.type==0)
                    })
                    .catch(error => {
                        console.log(error)
                    })
            },
            /*
             * Get all notes in a ticket.
             */
            getNotes() {
                this.$ajax.get('/api/notes/' + this.ticket.id)
                    .then(res => {
                        this.notes = res.data.json_data
                        console.log(res)
                    })
                    .catch(err => {
                        console.log(err)
                    })
            },
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
        },
        beforeMount: function () {
            this.user_id = this.$user.get().id
        },
        mounted: function () {
            this.getMessages()
            this.getNotes()
        },
        components: {
            'message': Message,
            'note': Note,
            'message-original': MessageOriginal
        }
    }
</script>