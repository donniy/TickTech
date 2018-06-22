<template>
    <div class="course-container">
        <transition name="custom-classes-transition" enter-active-class="animated tada" leave-active-class="animated bounceOutRight">
            <div class="subbox">
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
                                        <label for="searchField">Search by title...</label>
                                        <md-input id="searchField" v-model="search" @input="searchOnTable" style="color = white; background-color = white;" />
                                    </md-field>
                                </md-table-toolbar>

                                <md-table-empty-state md-label="No tickets found" v-show="this.tickets.length > 0" :md-description="`No ticket found for this '${search}' query. Try a different search term.`">
                                </md-table-empty-state>
                                <md-table-empty-state md-label="No tickets in this course" v-show="this.tickets.length <= 0">
                                </md-table-empty-state>

                                <md-table-row md-delay="1000" slot="md-table-row" slot-scope="{ item }" class="tickettable" v-on:click="navTicket(item.id)"
                                    v-on:mouseover="showTicket(item.id)" v-bind:class="{'md-table-cell':true, 'activated':(item.id === ticketSum)}">
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
                    <b-button v-if="isTA" class="btn note-add-button btn btn-primary">Add students</b-button>
                    <b-button class="btn note-add-button btn btn-primary" @click="emailSettings" :to="''">Mail settings</b-button>
                    <b-button v-if="isSupervisor" class="btn note-add-button btn btn-primary" :to="''">Add TA's</b-button>

                </div>
                <p v-if="email_running">EMAIL IS RUNNING</p>
                <emodal v-if="showEmailModal" warning="Setup a fetcher to your mailinglist." @close="showEmailModal = false">
                </emodal>
            </div>
        </transition>
        <div v-if="false" class=s ummary-sub-container>
            <summodal @close="showSum = false, ticketSum = 0" v-for="ticket in tickets" v-if="ticket.id == ticketSum" v-bind:key="ticket.id"
                v-bind:ticket="ticket" class="singleTicket">
            </summodal>
        </div>
        <p v-if="email_running">EMAIL IS RUNNING</p>
        <emodal v-if="showEmailModal" warning="Setup a fetcher to your mailinglist." @close="showEmailModal = false">
        </emodal>
        <addusers v-if="wantsToAddUsers" v-bind:title="'Add students to this course'" v-bind:label_message="'Students:'" v-bind:api_path="this.addStudentsPath">

        </addusers>
        <addusers v-if="wantsToAddTa" v-bind:title="'Add TAs to this course'" v-bind:label_message="'TAs:'" v-bind:api_path="this.addTasPath">
        </addusers>
    </div>
</template>

<script>
    const toLower = text => {
        return text.toString().toLowerCase()
    }

    const searchByName = (items, term) => {
        if (term) {
            return items.filter(item => toLower(item.title).includes(toLower(term)))
        }

        return items
    }

    import SumModal from './TicketSummary.vue'
    import EmailModal from './EmailSettingsModal.vue'
    import addUsersModel from './addUsersModel.vue'

    export default {
        data() {
            return {
                search: "",
                searched: [],
                ticketSum: 0,
                tickets: [],
                labels: [],
                showSum: false,
                status: 'not set',
                label_filter: 'All',
                status_filter: 'All',
                sort_filter: "Most Recent",
                showEmailModal: false,
                email_running: false,
                wantsToAddUsers: false,
                wantsToAddTa: false,
                addTasPath: "",
                addStudentsPath: "",
                isSupervisor: false,
                course: {
                    'id': "",
                    'course_email': "",
                    'title': "",
                    'description': "",
                    'tas': [],
                    'supervisors': [],
                },
            }
        },
        methods: {
            showTicket(item) {
                this.ticketSum = item
            },
            navTicket(item) {
                this.$router.push("/ticket/" + item)
            },
            searchOnTable() {
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
            pushLocation(here) {
                this.$router.push(here)
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
                this.getLabels()
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
            /* Function that checks if the current user is a supervisor for this course.
             * This is used to determine the rights of a user. It checks the id of the user
             * to the ids of the supervisors of this course. If a match is found we
             * set the this variable of isSupervisor equal to true. That will be used
             * in a v-if statement.
             */
            checkIfSupervisor() {
                let supervisors = this.course.supervisors;
                let userid = this.$user.get().id
                let matches = supervisors.filter(supervisor => supervisor.id === userid)
                this.isSupervisor = matches.length === 1
            },
            getCourseInfo() {
                this.status = 'getting course information'
                const path = '/api/courses/single/' + this.$route.params.course_id
                this.$ajax.get(path)
                    .then(response => {
                        this.course = response.data.json_data
                        window.$current_course_id = this.course.id
                        this.status = 'Retrieved data'
                        this.addStudentsPath = '/api/courses/' + this.course.id + '/students'
                        this.addTasPath = '/api/courses/' + this.course.id + '/tas'
                        this.checkIfSupervisor()
                    })
                    .catch(error => {
                        console.log(error)
                        this.status = 'failed getting course information'
                    })
            },

            /* Shows the menu to upload a csv file with user data. */
            addStudents() {
                this.wantsToAddTa = false
                this.wantsToAddUsers = this.wantsToAddUsers === false
            },
            /* Shows the menu to upload a csv file with ta data. */
            addTas() {
                this.wantsToAddUsers = false
                this.wantsToAddTa = this.wantsToAddTa === false
            },
            sort_tickets(val) {
                if (val == "Most Recent")
                    this.tickets.sort((a, b) => a.timestamp > b.timestamp)
                else if (val == "Least Recent")
                    this.tickets.sort((a, b) => a.timestamp < b.timestamp)
                else if (val == "Created by")
                    this.tickets.sort((a, b) => a.user_id > b.user_id)
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
            'emodal': EmailModal,
            'summodal': SumModal,
            'addusers': addUsersModel,
        },
        created: function () {
            this.emailRunning()
        },
        watch: {
            // whenever showMadel changes, this function will run
            showEmailModal: function () {
                this.emailRunning()
            },
            sort_filter: function (val) {
                this.sort_tickets(val)
            }
        }
    }
</script>
