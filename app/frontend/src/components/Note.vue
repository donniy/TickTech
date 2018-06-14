<template>
    <div class="material-card note">
    	<button class="btn btn-close-note" @click="showModal = true">
                <i class="material-icons"> close </i>
            </button>

    	<h4> {{note.user_id}}: </h4>
    	<p> {{note.text}} </p>

    	<modal v-if="showModal" warning="Are you sure you want to remove this note?" @yes="closeNote()" @close="showModal = false"></modal>
    </div>
</template>


<script>
    import axios from 'axios'
    import Modal from './ClosePrompt.vue'

    const axios_csrf = axios.create({
    	headers: {
    		'X-CSRFToken': 'need_to_replace'
    	}
    });

    export default {
    	props: ['note'],
    	data: function() {
    		return {
    			showModal: false
    		};
    	},
    	methods: {
    		closeNote() {
    			const path = '/api/notes/' + this.note.id + '/close'
    			axios_csrf.post(path)
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
