<template>
    <transition name="modal">
        <div class="summary-container">
            <button class="btn btn-primary close-sum" @click="$emit('close')">
                x
            </button>
            <div class="summary-wrapper">

                <div class="summary-tab">
                    <div class="summary-header">
                        <h3>Beschrijving</h3>
                    </div>
                    <div class="summary-content">
                        <message
                            v-bind:user="{id: user_id}"
                            v-for="message in messages.slice(0,1)"
                            v-bind:key="message.id"
                            v-bind:message="message">
                        </message>
                    </div>
                </div>

                <div class="summary-tab middle">
                    <div class="summary-header">
                        <h3>Chat</h3>
                    </div>
                    <div class="summary-content">
                        <message
                            v-bind:user="{id: user_id}"
                            v-for="message in messages"
                            v-bind:key="message.id"
                            v-bind:message="message">
                        </message>
                    </div>
                </div>

                <div class="summary-tab">
                    <div class="summary-header">
                        <h3>Notities</h3>
                    </div>
                    <div class="summary-content">
                        <note
                            v-for="note in notes"
                            v-bind:key="note.id"
                            v-bind:note="note">
                        </note>
                    </div>
                </div>

            </div>
        </div>
    </transition>
</template>

<script>


import axios from 'axios'
import Message from './MessageSum.vue'
import Note from './NoteSum.vue'

export default {
    props: {
        ticket: Object,
    },
    data () {
        return {
            messages: [],
            user_id: 0,
            notes: [],
        }
    },
    methods: {
        getMessages () {
            const path = '/api/ticket/' + this.ticket.id + '/messages'
            axios.get(path)
            .then(response => {
                this.messages = response.data.json_data
            })
            .catch(error => {
                console.log(error)
            })
        },
        getNotes () {
            axios.get('/api/notes/'+ this.ticket.id)
            .then(res => {
                this.notes = res.data.json_data
                console.log(res)
            })
            .catch(err => {
                console.log(err)
            })
        }
    },
    beforeMount: function() {
        this.user_id = this.$user.get().id
    },
    mounted: function () {
        this.getMessages()
        this.getNotes()
    },
    components: {
        'message': Message,
        'note': Note
    }
}
</script>