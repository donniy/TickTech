<template>
    <div>
    <h2>Tickets van Student {{ $route.params.user_id }}</h2>
    <div>
      <template v-for="course in courses">
        <b-btn variant="primary" class="dropdown-button" v-b-toggle="'course-' + course.id">
          {{course.title}} </b-btn>
        <b-collapse :id="'course-' + course.id" class="mt-2">
            <b-card>
              <ticket
                    v-for="ticket in tickets"
                    v-bind:key="ticket.id"
                    v-bind:ticket="ticket"
                    v-bind:base_url="'/student/ticket/'"
                ></ticket>
            </b-card>
        </b-collapse>
      </template>
    </div>
    <div>
    <b-button class="create-button" href="/form" >New ticket</b-button>
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
            courses: [],
            status: 'not set'
        }
    },
    methods: {
        getTickets () {
            this.status = 'getting tickets'
            const path = '/api/user/' + this.$route.params.user_id + '/tickets'
            axios.get(path).then(response => {
                this.tickets = response.data.json_list
                this.status = 'Retrieved data'
                console.log(response.data.json_list)
                console.log(response)
            }).catch(error => {
                console.log(error)
                this.status = 'failed getting tickets'
            })
        },

        getCourses () {
            const path = '/api/user/' + this.$route.params.user_id + '/courses'
            axios.get(path).then(response => {
                this.courses = response.data.json_data
                console.log(response.data)
                console.log("Courses")
                console.log(response.data.json_data[0])
            }).catch(error => {
                console.log(error)
            })
        },

        created () {
            this.status = 'created'
            this.getTickets()
            this.getCourses()
        }
    },
    mounted: function () {
        this.created()
        this.$emit('tab-activate', 'my-tickets')
    },
    watch: {
        '$route': function() {
            this.created()
        }
    },
    components: {
        'ticket': Ticket,
    }
}

</script>
