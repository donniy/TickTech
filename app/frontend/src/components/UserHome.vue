<!-- UserHome.vue is the homepage for a logged in student. -->
<template>
<div class="container">
	<div class="md-layout welcome-header">
		<h2>Welcome back {{ $user.get().name }}</h2>
	</div>
	<div class="md-layout md-gutter wrapper md-size-20 md-small-size-100">
		<div class="md-layout-item" v-if="isTA">
			<md-content class="md-elevation-5">
				<md-subheader>Courses</md-subheader>

				<md-content class="md-scrollbar courses-section">
					<md-list class="md-triple-line">
						<course v-for="course in ta_courses" v-bind:key="course.id" v-bind:course="course"></course>
					</md-list>
				</md-content>

			</md-content>
		</div>
		<div class="md-layout-item" v-if="!isTA">
			<md-content class="md-elevation-5">
				<md-subheader>Tickets</md-subheader>

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

			<md-card md-with-hover class="md-elevation-5 md-raised md-primary create-ticket-section1" @click.native="$router.push('/ticket/submit')">
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
			notifications: [],
			amount: 0.0,
			experience: 0,
			level: 0,
			exp_to_next: 0,
		}
	},
	methods: {
		// Retrieve tickets.
		getTickets() {
			this.status = 'getting ticket'
			const path = '/api/user/tickets'
			this.$ajax.get(path).then(response => {
				this.tickets = response.data.json_data
			}).catch(error => {
				console.log(error)
			})
		},
		getCourses() {
			this.ta_courses = this.$user.get().ta
			if (this.ta_courses && this.ta_courses.length > 0) {
				this.isTA = true
				return;
			}
			this.isTA = false;
			this.ta_courses = []
		},
		// Retrieve notifications.
		getTodos() {
			this.$ajax.get('/api/user/notifications', response => {
				this.notifications = response.data.json_data
			})
		},
		setLevelProgress() {

			const path = '/api/user/getlevels'
			this.$ajax.get(path).then(response => {
				this.level = response.data.json_data['level']
				this.experience = response.data.json_data['experience'] - this.level_to_xp(this.level - 1)
				this.exp_to_next = this.level_to_xp(this.level) - this.level_to_xp(this.level - 1)

                console.log(this.experience, this.exp_to_next)
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
		// Retrieve all information.
		created() {
			this.status = 'created'
			this.getCourses()
			this.getTodos()
			this.getTickets()
			this.setLevelProgress()
		}
	},
	// Called when page is loaded.
	mounted: function() {
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
