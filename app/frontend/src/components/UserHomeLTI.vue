<!-- Student only userhome. -->
<template>
<div v-else-if="this.$lti.data.lti_session">
	<template v-if="isTA == false && isStudent == true">
		<div class="md-layout welcome-header">
			<h3>Welcome back {{ $user.get().name }}</h3>
		</div>
		<div class="md-layout center-display md-gutter">
			<div class="md-layout-item md-size-50">
				<div class="md-layout-item">
					<md-content class="md-elevation-5 ticket-container">
						<md-subheader>My Submitted Tickets</md-subheader>
						<md-content class="md-layout center-display">
							<md-field class="md-layout-item md-size-90 ">
								<label for="courseFilter">Filter by course</label>
								<md-select id="courseFilter" v-model="selectedcourse">
									<md-option default value="">All courses</md-option>
									<md-option v-bind:value="course.id" v-bind:key="course.id" v-for="course in student_courses">{{course.title}}</md-option>
								</md-select>
							</md-field>
							<md-field md-clearable class="md-layout-item md-size-90 md-toolbar-section-end">
								<label for="searchField">Search by title...</label>
								<md-input id="searchField" v-model="search" style="color = white; background-color = white;" />
							</md-field>
						</md-content>
						<md-content class="md-scrollbar">
							<md-list>
								<md-list-item v-bind:key="ticket.id" v-for="ticket in filteredItems">
									<ticket v-bind:ticket="ticket"></ticket>
								</md-list-item>
							</md-list>
						</md-content>
					</md-content>
				</div>
			</div>
			<div class="md-layout-item md-size-35">
				<md-content class="md-elevation-5">
					<md-content class="md-scrollbar notification-section-47">
						<md-subheader>Notifications</md-subheader>
						<p style="padding-left: 16px;" v-if="notifications.length < 1">No notifications</p>
						<template v-for="notification in notifications">
                            <md-ripple>
                                <md-list-item :to="{name: (notification.ta ? 'SingleTicket' : 'StudentTicket'), params: {ticket_id: notification.ticket.id}}">
                                    <div class="md-list-item-text">
                                        <span>{{notification.ticket.title}}</span>
                                        <span>{{notification.ticket.message}}</span>
                                    </div>
                                    <md-badge class="md-primary" :md-content="notification.n" />
                                </md-list-item>
                            </md-ripple>
                        </template>
                   </md-content>
              </md-content>
              <md-card v-if="$user.isStudent()" md-with-hover class="md-elevation-5 md-raised md-primary create-ticket-section1" @click.native="$router.push('/ticket/submit')">
                  <md-ripple>
        			<md-card-content class="create-ticket-section2">
        				<h3 style="opacity:1;">Create ticket</h3>
        			</md-card-content>
        		  </md-ripple>
              </md-card>
          </div>
      </div>
  </template>

<!-- TA only userhome. -->
<template v-if="(isTA == true || isSupervisor == true) && isStudent == false">
	<div class="container">
		<div class="md-layout welcome-header">
			<h3>Welcome back {{ $user.get().name }}</h3>
		</div>
		<div class="md-layout center-display md-gutter">
			<div class="md-layout-item md-size-60">
				<div class="md-layout-item">
					<md-content class="md-elevation-5 ticket-container-small">
						<md-subheader>Tickets I'm assigned to</md-subheader>
						<md-content class="md-layout center-display">
							<md-field md-clearable class="md-layout-item md-size-90 md-toolbar-section-end">
								<label for="searchField">Search by title...</label>
								<md-input id="searchField" v-model="search" style="color = white; background-color = white;" />
							</md-field>
						</md-content>
						<md-content class="md-scrollbar">
							<md-list>
								<md-list-item v-bind:key="ticket.id" v-for="ticket in filteredItems">
									<taticket v-bind:ticket="ticket"></taticket>
								</md-list-item>
							</md-list>
						</md-content>
					</md-content>
					<md-content>
						<md-card class="md-elevation-5 level-container">
							<md-card-content class="md-size-100 center-display md-layout-item">
								<h5 class="md-title">Teaching assistant level {{this.level}} <md-tooltip md-direction="bottom"> Earn experience by being a helpful TA</md-tooltip></h5>
								<p class="md-caption">{{rank}}</p>
								<md-progress-bar md-mode="determinate" :md-value="amount"></md-progress-bar>
								<div v-if="this.experience == 0" class="md-subhead">Start helping people to earn experience</div>
								<div v-if="this.experience != 0" class="md-subhead">{{this.experience}}/{{this.exp_to_next}} experience to next level</div>
							</md-card-content>
						</md-card>
					</md-content>
				</div>
			</div>
			<div class="md-layout md-size-40">
				<div class="md-layout-item">
				<md-content class="md-layout-item md-elevation-5 notification-container-medium">
					<md-subheader>Notifications</md-subheader>
					<p style="padding-left: 16px;" v-if="notifications.length < 1">No notifications</p>
                        <template v-for="notification in notifications">
	                        <md-ripple>
		                         <md-list-item :to="{name: (notification.ta ? 'SingleTicket' : 'StudentTicket'), params: {ticket_id: notification.ticket.id}}">
		                              <div class="md-list-item-text">
	                                       <span>{{notification.ticket.title}}</span>
		                                   <span>{{notification.ticket.message}}</span>
		                              </div>
		                              <md-badge class="md-primary" :md-content="notification.n" />
								 </md-list-item>
							</md-ripple>
						</template>
                    </md-content>
                </div>
            </div>
        </div>
    </div>
</template>
</div>
</template>

<template>
<div class="container" v-else-if="this.$lti.data.lti_session">
	<div class="md-layout welcome-header">
		<h2>Welcome back {{ $user.get().name }}</h2>
	</div>
	<div class="md-layout md-gutter wrapper md-size-20 md-small-size-100">
		<div class="md-layout-item" v-if="isStudent">
			<md-content class="md-elevation-5">
				<md-subheader>Your tickets in this course</md-subheader>

				<md-content class="md-scrollbar courses-section">
					<md-list class="md-triple-line">

						<ticket v-for="ticket in tickets" v-bind:key="ticket.id" v-bind:ticket="ticket"></ticket>

					</md-list>
				</md-content>

			</md-content>
		</div>
		<div class="md-layout-item" v-if="isTA || isTeacher">
			<md-content class="md-elevation-5">
				<md-subheader>Tickets in this course, concerning you</md-subheader>

				<md-content class="md-scrollbar courses-section">
					<md-list class="md-triple-line">

						<ticket v-for="ticket in tickets" v-bind:key="ticket.id" v-bind:ticket="ticket" v-bind:TA_view="true">
						</ticket>

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
			<md-content>
				<md-card class="md-elevation-5 create-ticket-section1">
					<md-card-content v-if="isTA" class="md-gutter md-size-100 center-display md-layout-item">
						<h5 class="md-title">Teaching assistant level {{this.level}} <md-tooltip md-direction="bottom"> Earn experience by being a helpful TA</md-tooltip></h5>

						<br/>
						<md-progress-bar md-mode="determinate" :md-value="amount"></md-progress-bar>
						<div class="md-subhead">{{this.experience}}/{{this.exp_to_next}} experience to next level</div>
					</md-card-content>
				</md-card>
			</md-content>

			<!-- A TA can not create a ticket in an LTI session. -->
			<md-card md-with-hover v-if="isTA || isTeacher" class="md-elevation-5 md-raised md-primary create-ticket-section1" @click.native="$router.push('/course/' + lti_course.id)">
				<md-ripple>
					<md-card-content class="create-ticket-section2" style="display: block;" v-if="this.unassigned > 0">
						<h1 style="opacity:1;">Course overview </h1>
						<p style="align:center; padding-left:25%;">
							There are {{ this.unassigned}} unassigned tickets
						</p>
					</md-card-content>

					<md-card-content class="create-ticket-section2" v-if="this.unassigned == 0">
						<h1 style="opacity:1;">Course overview </h1>
					</md-card-content>
				</md-ripple>
			</md-card>

			<md-card md-with-hover v-if="isStudent" class="md-elevation-5 md-raised md-primary create-ticket-section1" @click.native="$router.push('/ticket/submit')">
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
            search: '',
            notifications: [],
            lti_course: null,
            unassigned: 0,
            amount: 0.0,
			      experience: 0,
			      level: 0,
			      exp_to_next: 0,
        }
    },
    methods: {
        /*
         * Function that gets the ticket for this lti course.
         * The api call depends on the role of the user.
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

        /*
         * Helper function to check if course is the current lti course.
         */
        is_lti_course(course) {
            return this.lti_course_id === course.id
        },

        /*
         * Function that gets the unassigned tickets in this course.
         * Is used to show a badge with updates for the course overview.
         */
        getCourseUnassignedTickets() {
            const path = '/api/courses/' + this.lti_course_id + '/tickets/unassigned';
            this.$ajax.get(path).then(response => {
                this.unassigned = response.data.json_data.length
            })
        },

        /*
         * Get the notifications for for this lti course,
         * for the current user.
         */
        getTodos() {
            this.$ajax.get(
                '/api/user/notifications?course_id='
                    + this.lti_course_id,
                response => {
                    this.notifications = response.data.json_data
                })
        },

        /*
         * Gets the current lti course from the user object,
         * based on the lti session.
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
            } else if (this.isTeacher) {
                let teacher_courses = this.$user.get().supervisor;
                this.lti_course = teacher_courses.find(this.is_lti_course);
                this.getCourseUnassignedTickets();
            }
        },

        /*
         * Function that determines the role of a user.
         * The ui of the site gets adapted to the role.
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
        setLevelProgress() {

			      const path = '/api/user/getlevels'
			      this.$ajax.get(path).then(response => {
				        this.level = response.data.json_data['level']
				        this.experience = response.data.json_data['experience'] - this.level_to_xp(this.level - 1)
				        this.exp_to_next = this.level_to_xp(this.level) - this.level_to_xp(this.level - 1)

				        // Set the level progress
				        this.amount = Math.round(100 * (this.experience / this.exp_to_next))

			      }).catch(error => {
				        console.log(error)
			      })

			      return
		    },
		    equate(xp) {
			      return Math.floor(xp + 300 * Math.pow(2, xp / 7));
		    },
		    level_to_xp(level) {
			      var xp = 0;

			      for (var i = 1; i < level; i++)
				        xp += this.equate(i);

			      return Math.floor(xp / 4);
		    },

        created() {
            this.determineRole()
            this.getLtiCourse();
            this.getTickets()
            this.getTodos();
            this.setLevelProgress()
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
    },
	computed: {
		filteredItems() {
			return this.tickets.filter(ticket => {
				return ticket.title.indexOf(this.search.toLowerCase()) > -1
			})
		},
	}
}
</script>
