<template>
    <div>
    <h2>Tickets van Student {{ $route.params.user_id }}</h2>
    <div>
        <b-btn variant="primary" v-b-toggle.collapseA>Course name {{ $route.params.course_id }}</b-btn>
        <b-collapse id="collapseA" class="mt-2">
            <b-card>
                <ticket
                    v-for="ticket in tickets"
                    v-bind:key="ticket.id"
                    v-bind:ticket="ticket"
                ></ticket>
            </b-card>
        </b-collapse>
    </div>
    <div>
    <b-button href="/form" >New ticket</b-button>
        </div>
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
      const path = '/api/user/' + this.$route.params.user_id
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
