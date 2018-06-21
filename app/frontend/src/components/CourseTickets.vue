<template>
    <div class = "course-container">
    <transition
    name="custom-classes-transition"
    enter-active-class="animated tada"
    leave-active-class="animated bounceOutRight"
    >
        <div class= "subbox">
            <div class="row">
                <div class="col-lg-12">
                    <h1>Course: {{ this.course.title }}</h1>
                    <br />
                    <hr style="width: 20%;">
                    <br />
                </div>
            </div>
            <div class="row">
                <div class="col-lg-12 col-md-12 text-center">
                    <div class="row">
                    <md-table v-model="searched" md-sort="name" md-sort-order="asc" md-card md-fixed-header class="white">
                      <md-table-toolbar class="red">
                        <h1 class="md-title">Tickets</h1>
                        <md-field md-clearable class="md-toolbar-section-end">
                            <md-input placeholder="Search by title..." v-model="search" @input="searchOnTable" style="color = white; background-color = white;"/>
                        </md-field>
                      </md-table-toolbar>

                      <md-table-empty-state
                        md-label="No tickets found"
                        :md-description="`No ticket found for this '${search}' query. Try a different search term.`">
                      </md-table-empty-state>

                      <md-table-row md-delay="1000" slot="md-table-row" slot-scope="{ item }" class="tickettable" v-on:click="navTicket(item.id)" v-on:mouseover="showTicket(item.id)" v-bind:class="{'md-table-cell':true, 'activated':(item.id === ticketSum)}">
                        <md-table-cell md-label="Title" md-sort-by="title" md-numeric>{{ item.title }}</md-table-cell>
                        <md-table-cell md-label="Name" md-sort-by="user_id">{{ item.user_id }}</md-table-cell>
                        <md-table-cell md-label="Status" md-sort-by="status.name">{{ item.status.name }}</md-table-cell>
                        <md-table-cell md-label="Time" md-sort-by="timestamp">{{ item.timestamp | moment("DD/MM/YY HH:mm")}}</md-table-cell>
                        <md-table-cell md-label="Operator" md-sort-by="binded_tas" v-if="item.binded_tas != null">{{ item.binded_tas }}</md-table-cell> 
                        <md-table-cell md-label="Operator" md-sort-by="binded_tas" v-if="item.binded_tas == null">unassigned</md-table-cell> 
                      </md-table-row>
                    </md-table>
                    </div>
                </div>
            </div>
            <div class="row">
                <b-button class="btn note-add-button btn btn-primary" button v-on:click="pushLocation('/course/' + $route.params.course_id + '/labels')">Course labels</b-button>
                <b-button class="btn note-add-button btn btn-primary" >Add students</b-button>
                <b-button class="btn note-add-button btn btn-primary" @click="emailSettings" :to="''">Mail settings</b-button>
                <b-button class="btn note-add-button btn btn-primary"  :to="''">Add TA's</b-button>

            </div>
            <p v-if="email_running">EMAIL IS RUNNING</p>
            <emodal v-if="showEmailModal" warning="Setup a fetcher to your mailinglist." @close="showEmailModal = false">
            </emodal>
        </div>
    </transition>
        <div class = summary-sub-container>
            <summodal @close="showSum = false, ticketSum = 0" v-for="ticket in tickets" v-if="ticket.id == ticketSum" v-bind:key="ticket.id"
                v-bind:ticket="ticket" class="singleTicket">
            </summodal>
        </div>
    </div>
</template>

<script>

    import CourseTicketRow from './CourseTicketRow.vue'
    import SumModal from './TicketSummary.vue'
    import EmailModal from './EmailSettingsModal.vue'

  const toLower = text => {
    return text.toString().toLowerCase()
  }

  const searchByName = (items, term) => {
    if (term) {
      return items.filter(item => toLower(item.title).includes(toLower(term)))
    }

    return items
  }

    export default {
        data() {
            return {
                search: null,
                searched: [],
                ticketSum: 0,
                tickets: [],
                showSum: false,
                status: 'not set',
                status_filter: 'All',
                showEmailModal: false,
                email_running: false,
                course: {
                    'id': "",
                    'course_email': "",
                    'title': "",
                    'description': "",
                    'tas': []
                }
            }
        },
        methods: {
            // mouseOver: function (one, two) {
            //     if (this.ticketSum != 0) {
            //         let className = one.path[1].className
            //         if (!(className.indexOf("singleTicket") > -1 || className.indexOf("summary") > -1)) {
            //             this.ticketSum = 0
            //             this.showSum = false
            //         }
            //     }
            // },
            showTicket (item) {
                this.ticketSum = item
            },
            navTicket (item) {
                this.$router.push("/ticket/" + item)
            },
            pushLocation(here) {
                this.$router.push(here)
            },
            searchOnTable () {
                this.searched = searchByName(this.tickets, this.search)
            },
            getTickets() {
                this.status = 'getting tickets'
                const path = '/api/courses/' + this.$route.params.course_id + '/tickets'
                this.$ajax.get(path)
                    .then(response => {
                        this.tickets = response.data.json_data
                        this.searched = this.tickets
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
            created() {
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
                    if (response.status == 201) {
                        // console.log("Here")
                        // console.log(response.data.json_data.running)
                        // console.log(response)
                        this.email_running = response.data.json_data.running
                    }
                })
            },
            getCourseInfo() {
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
            if (!this.$user.logged_in()) {
                this.$router.push('/login')
            }
            this.created();
        },
        beforemount() {
            this.searched = this.tickets
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