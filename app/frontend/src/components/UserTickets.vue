<template>
    <div>
    <h2>Tickets van Student {{ $route.params.user_id }}</h2>
    <div>
        <b-btn variant="primary" class="dropdown-button" v-b-toggle.collapseA>Arbitrary course name {{ $route.params.course_id }}</i></b-btn>
        <b-collapse id="collapseA" class="mt-2">
            <b-card>
                <ticket
                    v-for="ticket in tickets"
                    v-bind:key="ticket.id"
                    v-bind:ticket="ticket"
                    v-bind:base_url="'/student/ticket/'"
                ></ticket>
            </b-card>
        </b-collapse>
    </div>
    <div>
    <b-button class="create-button" href="/form" >New ticket</b-button>
        </div>
    </div>
</template>

<script>

import Vue from 'vue';
import axios from 'axios'
import Ticket from './Ticket.vue'
import VueCookies from 'vue-cookies';

Vue.use(VueCookies);

let axios_csrf = {};


export default {
  data () {
    return {
      tickets: [],
      status: 'not set'
    }
  },
  methods: {
    getTickets () {
      this.status = 'getting tickets';
      const path = '/api/user/active';
      axios_csrf.get(path)
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
    let hdr = {};

    let token = this.$cookies.get('token')
    
    if(token)
      hdr['Authorization'] = 'JWT ' + token;

    hdr['X-CSRFToken'] = csrf_token;
    axios_csrf = axios.create({
      headers: hdr
    });

    this.created()    
  },
  components: {
    'ticket': Ticket,
  }
}

</script>
