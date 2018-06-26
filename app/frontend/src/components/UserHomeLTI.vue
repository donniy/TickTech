<template>
<!-- When in LTI -->
    <div class="container" v-else-if="this.$lti.data.lti_session">
      <div class="md-layout welcome-header">
            <h2>Welcome back {{ $user.get().name }}</h2>
        </div>
        <div class="md-layout md-gutter wrapper md-size-20 md-small-size-100">
          <div class="md-layout-item" v-if="!isTA">
                <md-content class="md-elevation-5">
                        <md-subheader>Your tickets in this course</md-subheader>

                        <md-content class="md-scrollbar courses-section">
                        <md-list class="md-triple-line">

                            <ticket v-for="ticket in tickets" v-bind:key="ticket.id" v-bind:ticket="ticket"></ticket>

                        </md-list>
                        </md-content>

                </md-content>
          </div>
          <div class="md-layout-item" v-if="isTA">
                <md-content class="md-elevation-5">
                        <md-subheader>Tickets in this course, concerning you</md-subheader>

                        <md-content class="md-scrollbar courses-section">
                        <md-list class="md-triple-line">

                            <ticket v-for="ticket in tickets" v-bind:key="ticket.id" v-bind:ticket="ticket"></ticket>

                        </md-list>
                        </md-content>

                </md-content>
            </div>

            <div class="md-layout-item">
                <md-content class="md-elevation-5">
                    <md-list class="md-double-line padding-bottom-0">
                        <md-subheader>Notifications</md-subheader>

                        <md-content class="md-scrollbar notification-section">
                            <template v-for="notification in notifications">
                                <p style="padding-left: 16px;" v-if="tickets.length < 1">No notifications</p>
                                <md-ripple>
                                    <md-list-item :to="{name: (notification.ta ? 'SingleTicket' : 'StudentTicket'), params: {ticket_id: notification.ticket.id}}">
                                        <div class="md-list-item-text">
                                            <span>{{notification.ticket.title}}</span>
                                            <span>{{notification.ticket.message}}</span>
                                        </div>
                                        <md-badge class="md-primary" :md-content="notification.n" />

                                    </md-list-item>
                                </md-ripple>

                                <md-divider></md-divider>
                            </template>
                        </md-content>

                    </md-list>
                </md-content>
                <!-- A TA can not create a ticket in an LTI session. -->
                <md-card md-with-hover
                         v-if="isTA || isTeacher"
                         class="md-elevation-5 md-raised md-primary create-ticket-section1"
                         @click.native="$router.push('/course/' + lti_course.id)">
                    <md-ripple>
                        <md-card-content class="create-ticket-section2">
                          <h1 style="opacity:1;">Course overview</h1>
                          <md-badge v-bind:md-content="this.unassigned"> </md-badge>
                        </md-card-content>
                    </md-ripple>
                </md-card>

                <md-card md-with-hover
                         v-if="isStudent"
                         class="md-elevation-5 md-raised md-primary create-ticket-section1"
                         @click.native="$router.push('/ticket/submit')">
                    <md-ripple>
                        <md-card-content class="create-ticket-section2">
                            <h1 style="opacity:1;">Create ticket</h1>
                        </md-card-content>
                    </md-ripple>
                </md-card>
            </div>
        </div>
    </div>
</template>

<script>
import Course from './Course.vue'
import Ticket from './Ticket.vue'

export default {
    data() {
        return {
            ta_courses: [],
            status: 'not set',
            tickets: [],
            isTA: false,
            isTeacher: false,
            isStudent: false,
            notifications: [],
            lti_course: null,
            unassigned: 0,
        }
    },
    methods: {
        /* Function that gets the ticket for this lti course.
           The api call depends on the role of the user.
         */
        getTickets() {
            if (this.isTA || this.isTeacher) {
                const path = '/api/ta/courses/' + this.lti_course.id + '/tickets'
                this.$ajax.get(path).then(response => {
                    this.tickets = response.data.json_data
                })
                return;
            }
				    this.status = 'getting ticket'
				    const path = '/api/user/tickets/course/' + this.lti_course.id
				    this.$ajax.get(path).then(response => {
					      this.tickets = response.data.json_data
				    }).catch(error => {
					      console.log(error)
				    })
			  },

        /* Helper function to check if course is the current lti course. */
        is_lti_course(course) {
            return this.lti_course_id === course.id
        },

        /* Function that gets the unassigned tickets in this course.
           Is used to show a badge with updates for the course overview.
         */
        getCourseUnassignedTickets() {
            const path = '/api/courses/' + this.lti_course_id + '/tickets/unassigned';
            this.$ajax.get(path).then(response => {
                this.unassigned = response.data.json_data.length
            })
        },

        // Retrieve notifications.
        getTodos() {
            this.$ajax.get('/api/user/notifications', response => {
                console.log(response.data.json_data)
                this.notifications = response.data.json_data
            })
        },

        /* Gets the current lti course from the user object,
           based on the lti session.
         */
        getLtiCourse() {
            let lti_data = this.$lti.data.lti_data;
            this.lti_course_id = lti_data['tiktech_course_id'];
            if (this.isTA) {
                let courses_ta = this.$user.get().ta;
                this.lti_course = courses_ta.find(this.is_lti_course);
                this.getCourseUnassignedTickets();
            } else if (this.isStudent) {
                let student_courses = this.$user.get().student
                this.lti_course = student_courses.find(this.is_lti_course);
                console.log(this.lti_course)
            } else if (this.isTeacher) {
                let teacher_courses = this.$user.get().supervisor;
                this.lti_course = teacher_courses.find(this.is_lti_course);
                this.getCourseUnassignedTickets();
            }
        },

        /* Function that determines the role of a user.
           The ui of the site gets adapted to the role.
         */
        determineRole() {
            let lti_data = this.$lti.data.lti_data;
            if (lti_data['tiktech_is_course_TA']) {
                this.isTA = true;
            } else if (lti_data['tiktech_is_course_student']) {
                this.isStudent = true;
            } else if (lti_data['tiktech_is_course_teacher']) {
                this.isTeacher = true;
            }
        },

        created() {
            this.determineRole()
            this.getLtiCourse();
            this.getTickets()
            this.getTodos();
            this.status = 'created'
        }
    },
    mounted: function () {
        if (!this.$user.logged_in()) {
            this.$router.push('/login')
        }
        this.created();
    },
    components: {
        'course': Course,
        'ticket': Ticket
    }
}
</script>
