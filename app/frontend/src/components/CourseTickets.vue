<template>
    <div>
        <h1>Tickets in cursus {{ $route.params.course_id }}</h1>

        Status:
        <select v-model="status_filter">
            <option> All </option>
            <option> Needs help </option>
            <option> Answered </option>
        </select>

        <ticket
            v-for="ticket in tickets"
            v-if="status_filter == 'All' || ticket.status.name == status_filter"
            v-bind:key="ticket.id"
            v-bind:ticket="ticket"
        ></ticket>
    <b-button class="labelbutton:right" v-bind:href="'/course/'+ $route.params.course_id + '/labels'">Course labels</b-button>
    </div>
</template>

<script>

import axios from 'axios'
import Ticket from './Ticket.vue'

export default {
  data () {
    return {
      tickets: [],
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
  }
}

</script>
