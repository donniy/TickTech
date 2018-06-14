<template>
    <div>
        <h1>Tickets in cursus {{ $route.params.course_id }}</h1>
        Status:
        <select class="form-control custom-select" v-model="status_filter">
            <option> All </option>
            <option> Needs help </option>
            <option> Answered </option>
        </select>
        <b-button class="labelbutton:right" v-bind:href="'/course/'+ $route.params.course_id + '/labels'">Course labels</b-button>
        <button v-on:click="emailSettings" class="btn btn-primary">Email settings</button>

        <modal v-if="showModal" warning="Setup a fetcher to your mailinglist." @close="showModal = false"></modal>
        <p v-if="email_running">EMAIL IS RUNNING</p>
        <br /><br />

        <ticket
            v-for="ticket in tickets"
            v-if="status_filter == 'All' || ticket.status.name == status_filter"
            v-bind:key="ticket.id"
            v-bind:ticket="ticket"
        ></ticket>
    </div>
</template>

<script>

import Ticket from './Ticket.vue'
import Modal from './EmailSettingsModal.vue'
import axios from 'axios'

export default {
  data () {
    return {
      tickets: [],
      showModal: false,
      status: 'not set',
      status_filter: 'All',
      email_running: false
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
    emailSettings() {
        this.showModal = true
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
    created () {
      this.status = 'created'
      this.getTickets()
    }
  },
  mounted: function () {
    this.created()
  },
  components: {
    'ticket': Ticket,
    'modal': Modal
  },
  created: function () {
      this.emailRunning()
  },
  watch: {
    // whenever showMadel changes, this function will run
    showModal: function () {
        this.emailRunning()
    }
  },
}

</script>
