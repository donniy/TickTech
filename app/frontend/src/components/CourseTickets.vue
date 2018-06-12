<template>
    <div>
        <h1>Tickets in cursus {{ $route.params.course_id }}</h1>
        Status:
        <select class="form-control custom-select" v-model="status_filter">
            <option> All </option>
            <option> Needs help </option>
            <option> test </option>
        </select>
<<<<<<< HEAD
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
=======
        <b-button class="labelbutton:right" v-bind:href="'/course/'+ $route.params.course_id + '/labels'">Course labels</b-button>
        <button v-on:click="emailSettings" class="btn btn-primary">Email settings</button>

        <modal v-if="showModal" warning="Setup a fetcher to your mailinglist."
               @yes="updateEmail()" @close="showModal = false"></modal>
        <br /><br />

        <ticket
>>>>>>> master
            v-for="ticket in tickets"
            v-if="status_filter == 'All' || ticket.status.name == status_filter"
            v-bind:key="ticket.id"
            v-bind:ticket="ticket"
<<<<<<< HEAD
            ></ticket>
          </tbody>
        </table>
        </div>
        <modal 
        v-if="showModal" 
        @close="showModal = false"
        v-for-"ticket in tickets"
        v-if="ticket.id == 'ticketSum'"
        v-bind:key="ticketSum"
        v-bind:ticket="ticket"></modal>
=======
        ></ticket>
<<<<<<< HEAD
    <b-button class="labelbutton:right" v-bind:href="'/course/'+ $route.params.course_id + '/labels'">Course labels</b-button>
>>>>>>> master
=======
>>>>>>> master
    </div>
</template>

<script>

<<<<<<< HEAD
import axios from 'axios'
import TicketTA from './TicketTA.vue'
import Modal from './TicketSummary.vue'
=======
import Ticket from './Ticket.vue'
import Modal from './EmailSettingsModel.vue'
import axios from 'axios'
>>>>>>> master

export default {
  data () {
    return {
      ticketSum: 0,
      showModal: false,
      tickets: [],
      showModal: false,
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
    emailSettings() {
        this.showModal = true
    },
    updateEmail(form) {
        this.showModal = false
        console.log(form)
        const path = '/api/email'
        this.$ajax.post(path, form, response => {
            // TODO: Implement authentication on back-end to work with Canvas.
            console.log(response)
        })

    },
    stopEmail(form) {
        this.showModal = false
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
<<<<<<< HEAD
    'ticket': TicketTA,
    'modal' : Modal,
=======
    'ticket': Ticket,
    'modal': Modal
>>>>>>> master
  }
}

</script>
