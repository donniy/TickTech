<template>
    <div v-if="exists" class="material-card note">
        <md-button class="removeLabel" @click="showModal = true">
            <i class="material-icons"> close </i>
        </md-button>

    	<h4> {{note.user_id}}: </h4>
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
    		}
    	},
    	components: {
    		'modal': Modal
    	}
    }
</script>
