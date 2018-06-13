<template>
    <div>
        <h1>Tickets in cursus {{ $route.params.course_id }}</h1>

        <b-button class="labelbutton:right"
            v-on:click="goLabel('/course/'+ $route.params.course_id + '/labels')">
            Course labels
        </b-button>

        <button v-on:click="emailSettings" class="btn btn-primary">
            Email settings
        </button>

        <emodal v-if="showEmail"
                warning="Setup a fetcher to your mailinglist."
                @yes="updateEmail()"
                @close="showEmail = false">
        </emodal>

        <select class="form-control custom-select" v-model="status_filter">
            <option> All </option>
            <option> Needs help </option>
            <option> test </option>
        </select>

        <div class = TA-tickets>
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th scope="col">Title</th>
                        <th scope="col">Created by</th>
                        <th scope="col">Status</th>
                        <th scope="col">Date</th>
                    </tr>
                </thead>
                <tbody>
                    <ticket
                        v-for="ticket in tickets"
                        v-bind:class="{'tr-item':true, 'active':(ticket.id === ticketSum)}"
                        v-if="status_filter == 'All' || ticket.status.name == status_filter"
                        @click="ticketSum = ticket.id; Active"
                        v-bind:key="ticket.id"
                        v-bind:ticket="ticket"
                        v-bind:base_url="'/student/ticket/'">
                    </ticket>
                </tbody>
            </table>
        </div>
        
        <summodal
            @close="showSum = false, ticketSum = 0"
            v-for="ticket in tickets"
            v-if="ticket.id == ticketSum"
            v-bind:key="ticketSum"
            v-bind:ticket="ticket">
        </summodal>

    </div>
</template>

<script>

import axios from 'axios'
import TicketTA from './TicketTA.vue'
import SumModal from './TicketSummary.vue'
import EmailModal from './EmailSettingsModel.vue'

export default {
    data () {
        return {
            ticketSum: 0,
            showEmail: false,
            tickets: [],
            showSum: false,
            status: 'not set',
            status_filter: 'All'
        }
    },
    methods: {
        getTickets () {
            this.status = 'getting tickets'
            const path = '/api/courses/' + this.$route.params.course_id + '/tickets'
            axios.get(path)
            .then(response => {
                this.tickets = response.data.json_data
                this.status = 'Retrieved data'
                console.log(response.data.json_data)
                console.log(response)
            })
            .catch(error => {
                console.log(error)
                this.status = 'failed getting tickets'
            })
        },
        goLabel (here) {
            this.$router.push(here);
        },
        emailSettings() {
            this.showEmail = true
        },
        updateEmail(form) {
            this.showEmail = false
            console.log(form)
            const path = '/api/email'
            this.$ajax.post(path, form, response => {
                // TODO: Implement authentication on back-end to work with Canvas.
                console.log(response)
            })
        },
        stopEmail(form) {
            this.showEmail = false
            console.log(form)
            const path = '/api/email/stop'
            this.$ajax.post(path, form, response => {
                // TODO: Implement authentication on back-end to work with Canvas.
                console.log(response)
            })
        },
        created () {
            this.status = 'created'
            this.getTickets()
        }
    },
    mounted: function () {
        this.created()
    },
    components: {
        'ticket': TicketTA,
        'emodal': EmailModal,
        'summodal': SumModal
    }
}
</script>
