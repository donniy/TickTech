<!-- Student only userhome. -->
<template>
<div v-if="$auth.ready()">
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

	<!-- Hybride userhome. -->
	<template v-if="isTA == true && isStudent == true">
		<div class="container">
			<div class="md-layout welcome-header">
				<h3>Welcome back {{ $user.get().name }}</h3>
			</div>
			<div class="md-layout center-display md-gutter">
				<div class="md-layout-item md-size-60">
					<div class="md-layout-item">
						<md-tabs style="background-color: white;" class="md-elevation-5 ticket-container-small" md-sync-route md-alignment="fixed">
							<md-tab id="tab-student" md-label="Student tickets">
								<md-subheader>My Submitted Tickets</md-subheader>
								<div class="tab-layout">
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
								</div>
							</md-tab>
							<md-tab id="tab-ta" md-label="TA assigned tickets">
								<md-subheader>Tickets I'm assigned to</md-subheader>
								<div class="tab-layout">
									<md-content class="md-layout center-display">
										<md-field class="md-layout-item md-size-90 ">
											<label for="courseTAFilter">Filter by course</label>
											<md-select id="courseTAFilter" v-model="selectedTAcourse">
												<md-option default value="">All courses</md-option>
												<md-option v-bind:value="course.id" v-bind:key="course.id" v-for="course in ta_courses">{{course.title}}</md-option>
											</md-select>
										</md-field>
										<md-field md-clearable class="md-layout-item md-size-90 md-toolbar-section-end">
											<label for="searchTAField">Search by title...</label>
											<md-input id="searchTAField" v-model="searchTA" style="color = white; background-color = white;" />
										</md-field>
									</md-content>
									<md-content class="md-scrollbar">
										<md-list>
											<md-list-item v-bind:key="ticket.id" v-for="ticket in filteredTAItems">
												<ticket v-bind:ticket="ticket"></ticket>
											</md-list-item>
										</md-list>
									</md-content>
								</div>
							</md-tab>
						</md-tabs>
						<md-content>
							<md-card class="md-elevation-5 create-ticket-section1">
								<md-card-content class="md-gutter md-size-100 center-display md-layout-item">
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
					<md-content class="md-elevation-5 course-container-small">
						<md-subheader>Courses I'm TA in</md-subheader>

						<md-content class="md-scrollbar">
							<md-list class="md-triple-line">
								<course v-for="course in ta_courses" v-bind:key="course.id" v-bind:course="course"></course>
							</md-list>
						</md-content>

					</md-content>
					<md-content class="md-layout-item md-elevation-5 notification-container-small">
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
					<md-card md-with-hover class="md-elevation-5 md-raised md-primary create-ticket-section1" @click.native="$router.push('/ticket/submit')">
						<md-ripple>
							<md-card-content class="create-ticket-section2">
								<h3 style="opacity:1;">Create ticket</h3>
							</md-card-content>
						</md-ripple>
					</md-card>
				</div>
				</div>
			</div>
		</div>
	</template>

	<!-- TA only userhome. -->
	<template v-if="isTA == true && isStudent == false">
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
								<md-field class="md-layout-item md-size-90 ">
									<label for="courseTAFilter">Filter by course</label>
									<md-select id="courseTAFilter" v-model="selectedTAcourse">
										<md-option default value="">All courses</md-option>
										<md-option v-bind:value="course.id" v-bind:key="course.id" v-for="course in ta_courses">{{course.title}}</md-option>
									</md-select>
								</md-field>
								<md-field md-clearable class="md-layout-item md-size-90 md-toolbar-section-end">
									<label for="searchTAField">Search by title...</label>
									<md-input id="searchTAField" v-model="searchTA" style="color = white; background-color = white;" />
								</md-field>
							</md-content>
							<md-content class="md-scrollbar">
								<md-list>
									<md-list-item v-bind:key="ticket.id" v-for="ticket in filteredTAItems">
										<ticket v-bind:ticket="ticket"></ticket>
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
					<md-content class="md-elevation-5 course-container-medium">
						<md-subheader>Courses I'm TA in</md-subheader>

						<md-content class="md-scrollbar">
							<md-list class="md-triple-line">
								<course v-for="course in ta_courses" v-bind:key="course.id" v-bind:course="course"></course>
							</md-list>
						</md-content>

					</md-content>
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

<script>
import Course from './Course.vue'
import Ticket from './Ticket.vue'

export default {
	data() {
		return {
			ta_courses: [],
			status: 'not set',
			tickets: [],
			TAtickets: [],
			isTA: false,
			isStudent: false,
			notifications: [],
			amount: 0.0,
			experience: 0,
			level: 0,
			exp_to_next: 0,
			search: '',
			searchTA: '',
			selectedcourse: '',
			selectedTAcourse: '',
			student_courses: [],
			rank: ''
		}
	},
	methods: {
		/*
		 * Get all tickets.
		 */
		getTickets() {
			this.status = 'getting ticket'
			const path = '/api/user/tickets'
			this.$ajax.get(path).then(response => {
				if (typeof response.data.json_data !== 'undefined') {
					this.tickets = response.data.json_data
				}
			}).catch(error => {
				console.log(error)
			})
		},
		getTaTickets() {
			const path = '/api/ticket/gettatickets'
			this.$ajax.get(path).then(response => {
				if (typeof response.data.json_data !== 'undefined') {
					this.TAtickets = response.data.json_data
				}
			}).catch(error => {
				console.log(error)
			})
		},
		/*
		 * Get all courses a TA is bound to.
		 */
		getTaCourses() {
			this.ta_courses = this.$user.get().ta
			if (this.ta_courses && this.ta_courses.length > 0) {
				this.isTA = true
				return;
			}
			this.isTA = false;
			this.ta_courses = []
		},
		/*
		 * Get the rank of a TA
		 */
		 getRanking() {
             if (this.level) {
                 if (this.level < 5) {
                     this.rank = "Novice TA (" + this.level + ")"
                 } else if (this.level < 10) {
                     this.rank = "Adept TA (" + this.level + ")"
                 } else if (this.level < 15) {
                     this.rank = "Advancing TA (" + this.level + ")"
                 } else if (this.level < 18) {
                     this.rank = "Advanced TA (" + this.level + ")"
                 } else if (this.level < 23) {
                     this.rank = "Advanced'st TA (" + this.level + ")"
                 } else if (this.level < 28) {
                     this.rank = "Advanced'st've TA (" + this.level + ")"
                 } else if (this.level < 30) {
                     this.rank = "Powerfull TA (" + this.level + ")"
                 } else if (this.level < 38) {
                     this.rank = "Dr. TikTech (" + this.level + ")"
                 } else if (this.level < 45) {
                     this.rank = "No-lifer (" + this.level + ")"
                 } else if (this.level < 55) {
                     this.rank = "Question master (" + this.level + ")"
                 } else if (this.level < 60) {
                     this.rank = "Dr. Prof. TikTech (" + this.level + ")"
                 } else if (this.level < 65) {
                     this.rank = "TA Lord (" + this.level + ")"
                 } else if (this.level < 70) {
                     this.rank = "Teaching Elder (" + this.level + ")"
                 } else if (this.level < 75) {
                     this.rank = "TikTechian (" + this.level + ")"
                 } else if (this.level < 85) {
                     this.rank = "Mega-TikTechian (" + this.level + ")"
                 } else if (this.level < 90) {
                     this.rank = "Super-Mega-TikTechian (" + this.level + ")"
                 } else if (this.level < 95) {
                     this.rank = "The Oracle (" + this.level + ")"
                 } else if (this.level < 99) {
                     this.rank = "The One who Answers (" + this.level + ")"
                 } else {
                     this.rank = "Master of TikTech (" + this.level + ")"
                 }
             } else {
				 this.rank = "Rookie TA (" + this.level + ")"
			 }
         },
		/*
		 * Get all notifications.
		 */
		getTodos() {
			this.$ajax.get('/api/user/notifications', response => {
				this.notifications = response.data.json_data
			})
		},
		/*
		* Get all courses for this user
		*/
		getStudentCourses() {
            const pathCourses = '/api/user/student_courses'

            this.$ajax.get(pathCourses)
                .then(response => {
                    if (typeof response.data.json_data !== 'undefined') {
                        for (let i = 0; i < response.data.json_data.length; i++) {
                            let dataObj = response.data.json_data[i]
                            this.student_courses.push(dataObj)
                        }
						if (this.student_courses && this.student_courses.length > 0) {
							this.isStudent = true
							return
						}
						this.isStudent = false
						this.student_courses = []
                    }
                }).catch(error => {
                    console.log(error)
                })
		},
		/*
		 * Add xp to the user and set possible next level.
		 */
		setLevelProgress() {

			const path = '/api/user/getlevels'
			this.$ajax.get(path).then(response => {
				this.level = response.data.json_data['level']
				this.experience = response.data.json_data['experience'] - this.level_to_xp(this.level - 1)
				this.exp_to_next = this.level_to_xp(this.level) - this.level_to_xp(this.level - 1)

				// Set the level progress
				this.amount = Math.round(100 * (this.experience / this.exp_to_next))
				this.getRanking()

			}).catch(error => {
				console.log(error)
			})

			return
		},
		/*
		 * calculate new xp level.
		 */
		equate(xp) {
			return Math.floor(xp + 300 * Math.pow(2, xp / 7));
		},
		/*
		 * Calculate xp needed for a specific level.
		 */
		level_to_xp(level) {
			var xp = 0;

			for (var i = 1; i < level; i++)
				xp += this.equate(i);

			return Math.floor(xp / 4);
		},
		/*
		 * Retrieve all information.
		 */
		created() {
			this.status = 'created'
			if (this.$user.get().ta) {

				this.getTaCourses()
				this.getTaTickets()
				this.setLevelProgress()
			}
			if (this.$user.isStudent) {
				console.log("STUDENT")
				this.getStudentCourses()
				this.getTickets()
			}
			this.getTodos()
		}
	},
	/*
	 * Called when page is loaded.
	 */
	mounted: function() {
		if (!this.$user.logged_in()) {
			this.$router.push('/login')
		}
		this.created()
	},
	components: {
		'course': Course,
		'ticket': Ticket
	},
	computed: {
	    filteredItems() {
			if (this.selectedcourse === "") {
				return this.tickets.filter(ticket => {
					return ticket.title.indexOf(this.search.toLowerCase()) > -1
				})
			} else {
				return this.tickets.filter(ticket => {
					return (ticket.title.indexOf(this.search.toLowerCase()) > -1) && (ticket.course.id == this.selectedcourse)
				})
			}
		},
		filteredTAItems() {
			if (this.selectedTAcourse === "") {
				return this.TAtickets.filter(ticket => {
					return ticket.title.indexOf(this.searchTA.toLowerCase()) > -1
				})
			} else {
				return this.TAtickets.filter(ticket => {
					return (ticket.title.indexOf(this.searchTA.toLowerCase()) > -1) && (ticket.course.id == this.selectedTAcourse)
				})
			}
		}
  	},
	watch: {
		selectedcourse: function () {
			this.search = ''
		}
	}
}
</script>
