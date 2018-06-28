<template>
    <div>
        <router-link style="float:left;" to="/home">Back to home</router-link>
        <div>
            <h3 style="text-align:center">Your tickets: {{ this.$user.get().name }}</h3>
            <hr>
            </br>
        </div>
        <div class="ticket-container">
            <template v-for="course in courses">
                <b-btn variant="primary" class="dropdown-button" v-b-toggle="'course-' + course.id">
                  {{course.title}} </b-btn>
                <b-collapse accordion="my-accordion" :id="'course-' + course.id" class="mt-2">
                    <p v-if="tickets.length < 1">- No Tickets yet -</p>
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
    </div>
</template>

<script>
    import Vue from 'vue'
    import Ticket from './Ticket.vue'
    import VueCookies from 'vue-cookies'


    export default {
        data() {
            return {
                tickets: [],
                courses: [],
                status: 'not set'
            }
        },
        methods: {
            /*
             * Get all tickets for a specific user.
             */
            getTickets() {
                this.status = 'getting tickets'
                const path = '/api/user/' + this.$user.get().id + '/tickets'
                this.$ajax.get(path).then(response => {
                    this.tickets = response.data.json_data
                    this.status = 'Retrieved data'
                    // console.log(response.data.json_data)
                    // console.log(response)
                }).catch(error => {
                    console.log(error)
                    this.status = 'failed getting tickets'
                })
            },
            /*
             * Get all courses for a specific user.
             */
            getCourses() {
                const path = '/api/user/' + this.$user.get().id + '/courses'
                this.$ajax.get(path).then(response => {
                    this.courses = response.data.json_data
                    // console.log(response.data)
                }).catch(error => {
                    console.log(error)
                })
            },

            created() {
                this.status = 'created'
                this.getTickets()
                this.getCourses()
            }
        },
        mounted: function () {
            if (!this.$user.logged_in()) {
                console.log("fuck")
                this.$router.push('/login')
            }

            this.created()
            this.$emit('tab-activate', 'my-tickets')
        },
        // watch: {
        //     '$route': function() {
        //         this.created()
        //     }
        // },
        components: {
            'ticket': Ticket,
        }
    }
</script>
