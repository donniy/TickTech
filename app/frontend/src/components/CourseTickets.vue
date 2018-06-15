<template>
    <div>
        <h1>Tickets</h1>
        <h2>{{ this.course.title }}</h2>

        <b-button class="labelbutton:right"
            v-on:click="goLabel('/course/'+ $route.params.course_id + '/labels')">
            Course labels
        </b-button>

        <button v-on:click="emailSettings" class="btn btn-primary">
            Email settings
        </button>

        <emodal v-if="showEmailModal"
                warning="Setup a fetcher to your mailinglist."
                @close="showEmailModal = false">
        </emodal>
        <p v-if="email_running">EMAIL IS RUNNING</p>

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

import CourseTicketRow from './CourseTicketRow.vue'
import SumModal from './TicketSummary.vue'
import EmailModal from './EmailSettingsModal.vue'

export default {
    data () {
        return {
            ticketSum: 0,
            tickets: [],
            showSum: false,
            status: 'not set',
            status_filter: 'All',
            showEmailModal: false,
            email_running: false,
            course : {
                'id': "",
                'course_email': "",
                'title': "",
                'description': "",
                'tas': []
            }
        }
    },
    methods: {
        getTickets () {
            this.status = 'getting tickets'
            const path = '/api/courses/' + this.$route.params.course_id + '/tickets'
            this.$ajax.get(path)
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
            this.showEmailModal = true
        },
        updateEmail(form) {
            this.showEmailModal = false
            console.log(form)
            const path = '/api/email'
            this.$ajax.post(path, form, response => {
                // TODO: Implement authentication on back-end to work with Canvas.
                console.log(response)
            })
        },
        stopEmail(form) {
            this.showEmailModal = false
            console.log(form)
            const path = '/api/email/stop'
            this.$ajax.post(path, form, response => {
                // TODO: Implement authentication on back-end to work with Canvas.
                console.log(response)
            })
        },
        created () {
            this.status = 'created'
            this.getCourseInfo()
            this.getTickets()
        },
        emailRunning: function () {
            // Get the current email settings from server
            // console.log("Check if email is running")
            const path = '/api/email/' + this.$route.params.course_id + '/online'
            this.$ajax.get(path, response => {
                // TODO: Implement authentication on back-end to work with Canvas.
                // console.log("repsone email running")
                // console.log(response)
                if (response.status == 201){
                    // console.log("Here")
                    // console.log(response.data.json_data.running)
                    // console.log(response)
                    this.email_running = response.data.json_data.running
                }
            });
        },
        getCourseInfo(){
            this.status = 'getting course information'
            const path = '/api/courses/single/' + this.$route.params.course_id
            this.$ajax.get(path)
            .then(response => {
                this.course = response.data.json_data
                this.status = 'Retrieved data'
                console.log(response.data.json_data)
                console.log(response)
            })
            .catch(error => {
                console.log(error)
                this.status = 'failed getting course information'
            })
        }
    },
    mounted: function () {
        this.created()
    },
    components: {
        'ticket': CourseTicketRow,
        'emodal': EmailModal,
        'summodal': SumModal
    },
    created: function () {
        this.emailRunning()
    },
    watch: {
        // whenever showMadel changes, this function will run
        showEmailModal: function () {
            this.emailRunning()
        }
    },
}
</script>
