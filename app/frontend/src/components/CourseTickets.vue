<template>
    <div>
        <h1>Tickets in cursus {{ $route.params.course_id }}</h1>

        Status:
        <select v-model="status_filter">
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
            v-if="status_filter == 'All' || ticket.status.name == status_filter"
            v-bind:key="ticket.id"
            v-bind:ticket="ticket"
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
    </div>
</template>

<script>

import axios from 'axios'
import TicketTA from './TicketTA.vue'
import Modal from './TicketSummary.vue'

export default {
  data () {
    return {
      ticketSum: 0,
      showModal: false,
      tickets: [],
      status: 'not set',

      status_filter: 'All'
    }
  },
  methods: {
    getTickets () {
      this.status = 'getting tickets'
      const path = '/api/course/' + this.$route.params.course_id
      axios.get(path)
      .then(response => {
        this.tickets = response.data.json_list
        this.status = 'Retrieved data'
        console.log(response.data.json_list)
        console.log(response)
      })
      .catch(error => {
        console.log(error)
        this.status = 'failed getting tickets'
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
    'modal' : Modal,
  }
}

</script>
