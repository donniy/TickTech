<template>
    <div v-if="exists" class="material-card note">
        <md-button v-if="note.user_id == this.user.id" class="md-icon-button remove-note" @click="showModal = true">
            <i class="material-icons"> close </i>
        </md-button>
        <h5> {{this.user.name}}: </h5>
        <p> {{note.text}} </p>

        <md-dialog  :md-active.sync="showModal">
            <md-dialog-title>Do you want to remove this note?</md-dialog-title>
            <md-dialog-actions>
                <md-button class="md-primary" @click="showModal = false">Nope</md-button>
                <md-button class="md-primary" @click="closeNote()">Yes I'm sure</md-button>
            </md-dialog-actions>
        </md-dialog>
    </div>
</template>


<script>
    import Modal from './ClosePrompt.vue'

    export default {
    	props: ['note'],
    	data: function() {
    		return {
    			showModal: false,
                exists: true,
                user: ''
            }
        },
        methods: {
            closeNote() {
                const path = '/api/notes/' + this.note.id + '/close'
                this.$ajax.post(path)
                    .then(response => {
                        this.showModal = false
                    })
                this.exists = false
                this.$parent.getNotes()
            },
            getUser() {
                const path = '/api/user/' + this.note.user_id
                this.$ajax.get(path)
                    .then(response => {
                        this.user = response.data.json_data
                    })
            }
        },
        components: {
            'modal': Modal
        },
        mounted: function() {
            this.getUser()
        }
    }
</script>
