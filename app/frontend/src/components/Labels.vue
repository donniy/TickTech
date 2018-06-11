<template>
    <div>
        <div>
            <section>
                <h1>Create and assign labels</h1>
                <button v-on:click="createLabel" class="labelbutton-left">Create new</button>
                <b-button class="labelbutton-right">Save</b-button>
            </section>
        </div>
        <div>
            <ticketlabel
               v-for="label in labels"
               v-bind:key="label.label_id"
               v-bind:label="label">
            </ticketlabel>
        </div>
   </div>
</template>

<script>

import axios from 'axios'
import Ticket from './Ticket.vue'
import Ticketlabel from './Ticketlabel.vue'

const axios_csrf = axios.create({
  headers: {'X-CSRFToken': 'need_to_replace'}
});

export default {
    data () {
        return {
            status: 'not set',
            labels : [],
            label_name: 'Nope'
        }
    },
    methods: {
        getLabels () {
            this.status = 'getting labels'
            const path = '/api/labels/' + this.$route.params.course_id
            axios.get(path)
            .then(response => {
                this.labels = response.data.json_list
                this.status = 'Retrieved data'
                console.log(response.data.json_list)
                console.log(response)
            })
            .catch(error => {
                console.log(error)
                this.status = 'failed getting tickets'
            })
        },
        createLabel() {
            this.status = 'creating labels'
            const path = '/api/labels/' + this.$route.params.course_id
            axios_csrf.post(path, this.label_name)
            .then(response => {
                this.tickets = response.data.json_list
                this.status = 'Retrieved data'
                console.log(response.data.json_list)
                console.log(response)
                this.getLabels()
            })
            .catch(error => {
                console.log(error)
                this.status = 'failed getting tickets'
            })
        },
         created () {
            this.status = 'created'
            this.getLabels()
        }
    },
        mounted: function () {
            this.created()
    },
    components: {
         'ticketlabel': Ticketlabel
    }
}

</script>
