<template>
    <div>
        <h1>Tickets in {{ $route.params.course_id }}</h1>
        <ticket
            v-for="ticket in tickets"
            v-bind:key="ticket.id"
            v-bind:ticket="ticket"
        ></ticket>
    </div>
</template>

<script>

import axios from 'axios'
import Ticket from './Ticket.vue'

export default {
  data () {
    return {
      tickets: [],
      status: 'not set'
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
    'ticket': Ticket,
  }
}

</script>
