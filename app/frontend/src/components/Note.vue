<!-- Note.vue adds, shows, and removes secret notes to a ticket, only viewable for TA's.  -->
<template>
    <div class="material-card note">
        <button class="btn btn-close-note" @click="showModal = true">
            <i class="material-icons"> close </i>
        </button>
        <h4>{{note.user_id}}: </h4>
        <p> {{note.text}} </p>
        <modal v-if="showModal" warning="Are you sure you want to remove this note?" @yes="closeNote()" @close="showModal = false"></modal>
    </div>
</template>


<script>
    import Modal from './ClosePrompt.vue'

    export default {
        props: ['note'],
        data: function () {
            return {
                showModal: false
            }
        },
        methods: {
            // Removes a note.
            closeNote() {
                const path = '/api/notes/' + this.note.id + '/close'
                this.$ajax.post(path)
                    .then(response => {
                        this.showModal = false
                    })
                this.$parent.getNotes()
            }
        },
        components: {
            'modal': Modal
        }
    }
</script>