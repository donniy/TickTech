<template>
    <div v-on:mouseover="mouseOver">
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
                    <div class="col-lg-4 col-md-4 text-center">
                        <h5>Tickets in this course:</h5>
                    </div>
                    <div class="col-lg-4 col-md-4 text-center">
                        <select class="form-control custom-select" v-model="status_filter">
                            <option> All </option>
                            <option> Closed </option>
                            <option> Unassigned </option>
                            <option> Assigned </option>
                        </select>
                    </div>
                    <div class="col-lg-4 col-md-4 text-center">
                        <select class="form-control custom-select">
                            <option> Most recent </option>
                            <option> Created by </option>
                            <option> Least recent </option>
                        </select>
                    </div>
                </div>
                <div class=T A-tickets>
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
                            <ticket v-for="ticket in tickets" v-bind:class="{'tr-item':true, 'active':(ticket.id === ticketSum)}" v-if="status_filter == 'All' || ticket.status.name == status_filter"
                                @click="ticketSum = ticket.id; Active" v-bind:key="ticket.id" v-bind:ticket="ticket" v-bind:base_url="'/student/ticket/'">
                            </ticket>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-2 col-md-2 text-center">
                <b-button class="routerbutton" v-on:click="pushLocation('/course/' + $route.params.course_id + '/labels')">Course labels</b-button>
            </div>

            <div class="col-lg-2 col-md-2 text-center" >
                <b-button class="routerbutton" @click="addStudents" >Add students</b-button>

            </div>
            <div class="col-lg-2 col-md-2 text-center">
                <b-button class="routerbutton" @click="emailSettings" :to="''">Mail settings</b-button>
            </div>
            <div class="col-lg-2 col-md-2  text-center" v-if="isSupervisor">
                <b-button class="routerbutton" @click="addTas" :to="''">Add TA's</b-button>
            </div>

        </div>
        <p v-if="email_running">EMAIL IS RUNNING</p>
        <emodal v-if="showEmailModal" warning="Setup a fetcher to your mailinglist." @close="showEmailModal = false">
        </emodal>
        <summodal @close="showSum = false, ticketSum = 0" v-for="ticket in tickets" v-if="ticket.id == ticketSum" v-bind:key="ticket.id"
            v-bind:ticket="ticket" class="singleTicket">
        </summodal>

        <addusers v-if="wantsToAddUsers"
                  v-bind:title="'Add students to this course'"
                  v-bind:label_message="'Students:'"
                  v-bind:api_path="this.addStudentsPath">

        </addusers>
        <addusers v-if="wantsToAddTa"
                  v-bind:title="'Add TAs to this course'"
                  v-bind:label_message="'TAs:'"
                  v-bind:api_path="this.addTasPath">
        </addusers>
    </div>
</template>
<script>


import CourseTicketRow from './CourseTicketRow.vue'
import SumModal from './TicketSummary.vue'
import EmailModal from './EmailSettingsModal.vue'
import addUsersModel from './addUsersModel.vue'

export default {
    data () {
        return {
            ticketSum: 0,
            tickets: [],
            showSum: false,
            status: 'not set',
            status_filter: 'All',
            showEmailModal: false,
            email_running: false,
            wantsToAddUsers: false,
            wantsToAddTa: false,
            addTasPath: "",
            addStudentsPath: "",
            isSupervisor: false,
            course : {
                'id': "",
                'course_email': "",
                'title': "",
                'description': "",
                'tas': [],
                'supervisors': [],
            }
        }
    },
    methods: {
        pushLocation (here) {
            this.$router.push(here)
        },
        getTickets () {
            this.status = 'getting tickets'
            const path = '/api/courses/' + this.$route.params.course_id + '/tickets'
            this.$ajax.get(path)
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
        mouseOver: function (one, two) {
            if (this.ticketSum != 0) {
                let className = one.path[1].className
                if (!(className.indexOf("singleTicket") > -1 || className.indexOf("summary") > -1)) {
                    this.ticketSum = 0
                    this.showSum = false
                }
            }
        },
        pushLocation(here) {
            this.$router.push(here)
        },
        getTickets() {
            this.status = 'getting tickets'
            const path = '/api/courses/' + this.$route.params.course_id + '/tickets'
            this.$ajax.get(path)
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
        getCourseInfo(){
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
    },
    mounted: function () {
        if (!this.$user.logged_in()) {
            this.$router.push('/login')
        }
        this.created()
    },
    components: {
        'ticket': CourseTicketRow,
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
        }
    },
}
</script>
