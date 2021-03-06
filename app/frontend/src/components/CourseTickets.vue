<template>
<div>
	<div class="md-layout-item welcome-header">
		<h1>Course: {{ this.course.title }}</h1>
	</div>
	<div class="md-layout">
        <div class="md-layout-item md-size-80">
		<div class="md-layout-item md-size-100">
            <div class="md-layout-item">
			<md-table v-model="searched" md-sort="name" md-sort-order="asc" md-fixed-header class="white md-elevation-5 md-layout-item md-size-100">
				<md-table-toolbar class="red">

					<div class="col-lg-3 col-md-3 text-center">
						<select class="form-control custom-select" v-model="label_filter">
                        <option>Any label</option>
                        <option v-for="option in labels">{{option.label_name}}</option>
                    </select>
					</div>

					<div class="col-lg-3 col-md-3 text-center">
						<select class="form-control custom-select" v-model="status_filter">
                        <option>Any status</option>
                        <option>Unassigned</option>
                        <option>Closed</option>
                        <option>Assigned but waiting for reply</option>
                        <option>Receiving help</option>
                    </select>
					</div>

					<md-field md-clearable class="md-toolbar-section-end">
						<label for="searchField">Search by title...</label>
						<md-input autofocus id="searchField" v-model="search" @input="searchOnTable" style="color = white; background-color = white;" />
					</md-field>
				</md-table-toolbar>

				<md-table-empty-state md-label="No tickets found" v-show="this.tickets.length > 0" :md-description="`No ticket found for this '${search}' query. Try a different search term.`">
				</md-table-empty-state>
				<md-table-empty-state md-label="No tickets in this course" v-show="this.tickets.length <= 0">
				</md-table-empty-state>

				<md-table-row md-delay="1000" slot="md-table-row" slot-scope="{ item }" class="tickettable" v-on:click="navTicket(item.id)" v-on:mouseover="showTicket(item.id)" v-bind:class="{'md-table-cell':true, 'activated':(item.id === ticketSum)}">
					<md-table-cell md-label="Title" md-sort-by="title" md-numeric>{{item.title}}</md-table-cell>
					<md-table-cell md-label="Label" md-sort-by="label.label_name" md-numeric v-if="Object.keys(item.label).length != 0">{{item.label.label_name}}</md-table-cell>
					<md-table-cell md-label="Label" md-sort-by="label.label_name" md-numeric v-if="Object.keys(item.label).length === 0">No Label</md-table-cell>
					<md-table-cell md-label="Name" md-sort-by="user_id">{{item.user_id}}</md-table-cell>
					<md-table-cell md-label="Status" md-sort-by="status.name">{{item.status.name}}</md-table-cell>
					<md-table-cell md-label="Time" md-sort-by="timestamp">{{item.timestamp | moment("DD/MM/YY HH:mm")}}</md-table-cell>
				</md-table-row>
			</md-table>
        </div>
		</div>
		<div class="md-layout md-size-100">
			<md-content>
				<template v-if="isSupervisor">
                <md-content class="md-elevation-3">
                    <md-list>
                        <md-subheader>Plugins</md-subheader>

                        <plugin :key="pid" v-for="(plugin, pid) in plugins" :plugin="plugin" :pid="pid" />
                    </md-list>
                </md-content>
            </template>
			</md-content>
            <md-button class="btn btn btn-primary" button v-on:click="pushLocation('/course/' + $route.params.course_id + '/labels')">Course labels</md-button>
            <!-- <md-button v-if="isTA" class="btn btn btn-primary">Add students</md-button> -->
            <md-button class="btn btn btn-primary" @click="emailSettings" :to="''">Mail settings <md-icon class="email-running" v-if="email_running">email</md-icon><md-icon class="email-not-running" v-if="!email_running">mail_outline</md-icon></md-button>
            <!-- <md-button v-if="isSupervisor" class="btn btn btn-primary" :to="''">Add TA's</md-button> -->

            <emodal v-if="showEmailModal" warning="Setup a fetcher to your mailinglist." @close="showEmailModal = false">
            </emodal>
            <div class=summary-sub-container>
                <summodal v-show="false"@close="showSum = false, ticketSum = 0" v-for="ticket in tickets" v-if="ticket.id == ticketSum" v-bind:key="ticket.id" v-bind:ticket="ticket" class="singleTicket">
                </summodal>
            </div>
		</div>
    </div>
		<addusers v-if="wantsToAddUsers" v-bind:title="'Add students to this course'" v-bind:label_message="'Students:'" v-bind:api_path="this.addStudentsPath">

		</addusers>
		<addusers v-if="wantsToAddTa" v-bind:title="'Add TAs to this course'" v-bind:label_message="'TAs:'" v-bind:api_path="this.addTasPath">
		</addusers>
	</div>
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
import PluginsListItem from './PluginsListItem.vue'

export default {
	data() {
		return {
			timeout: 0,
			search: "",
			searched: [],
			ticketSum: 0,
			tickets: [],
			labels: [],
			showSum: false,
			status: 'not set',
			label_filter: 'Any label',
			status_filter: 'Any status',
			sort_filter: "Most Recent",
			showEmailModal: false,
			email_running: false,
			wantsToAddUsers: false,
			wantsToAddTa: false,
			addTasPath: "",
			addStudentsPath: "",
			isSupervisor: false,
			isTA: false,
			course: {
				'id': "",
				'course_email': "",
				'title': "",
				'description': "",
				'tas': [],
				'supervisors': [],
			},
			plugins: {}
		}
	},
	methods: {
		showTicket(item) {
			clearTimeout(this.timeout)
			this.timeout = setTimeout(() => {
				this.ticketSum = item
			}, 400)
		},
		navTicket(item) {
			this.$router.push("/ticket/" + item)
		},
		searchOnTable() {
			this.searched = searchByName(this.tickets, this.search)
		},

		/*
		 * Get all tickets from a specific course.
		 */
		getTickets() {
			this.status = 'getting tickets'
			const path = '/api/courses/' + this.$route.params.course_id + '/tickets'
			this.$ajax.get(path)
				.then(response => {
					this.tickets = response.data.json_data
					this.searched = this.tickets
					this.status = 'Retrieved data'
				})
				.catch(error => {
					console.log(error)
					this.status = 'failed getting tickets'
				})
		},
		getPlugins() {
			const path = '/api/courses/' + this.$route.params.course_id + '/plugins'
			this.$ajax.get(path, response => {
				this.plugins = response.data.json_data
			})
		},
		updatePluginState(data) {
			const path = '/api/courses/' + this.$route.params.course_id + '/plugins/' + data
			this.$ajax.patch(path, {
				active: this.plugins[data].active
			}, response => {
				console.log(response)
			})
		},

		/*
		 * Go to the corresponding label page from a course.
		 */
		pushLocation(here) {
			this.$router.push(here)
		},
		emailSettings() {
			this.showEmailModal = true
		},

		/*
		 * Fetch new emails from backend.
		 */
		updateEmail(form) {
			this.showEmailModal = false
			const path = '/api/email'
			this.$ajax.post(path, form, response => {
				// TODO: Implement authentication on back-end to work with Canvas.
			})
		},

		/*
		 * Stop the mail server in the backend.
		 */
		stopEmail(form) {
			this.showEmailModal = false
			const path = '/api/email/stop'
			this.$ajax.post(path, form, response => {
				// TODO: Implement authentication on back-end to work with Canvas.
			})
		},
		created() {
			this.status = 'created'
			this.getCourseInfo()
			this.getTickets()
			this.getPlugins()
			this.getLabels()
            if (this.$user.get().ta) {
                this.isTA = true
            }
		},
		emailRunning: function() {
			// Get the current email settings from server
			const path = '/api/email/' + this.$route.params.course_id + '/online'
			this.$ajax.get(path, response => {
				// TODO: Implement authentication on back-end to work with Canvas.
				if (response.status == 201) {
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

		/*
		 * Get all information from a specific course.
		 */
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
					this.$router.push('/home')
				})
		},

		/*
		 * Get all labels attached to a course.
		 */
		getLabels() {
			const path = '/api/labels/' + this.$route.params.course_id
			this.$ajax.get(path, response => {
				this.labels = response.data.json_data
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

		/*
		 * Logic to filter tickets by label or status.
		 */
		filter_tickets() {
			this.searched = this.tickets.filter(ticket => {
				return (ticket.label.label_name == this.label_filter || this.label_filter == "Any label") &&
					(ticket.status.name == this.status_filter || this.status_filter == "Any status")
			})
		}
	},
	mounted: function() {
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
		'plugin': PluginsListItem,
	},
	created: function() {
		this.emailRunning()
	},
	watch: {
		// whenever showMadel changes, this function will run
		showEmailModal: function() {
			this.emailRunning()
		},
		label_filter: function() {
			this.filter_tickets()
		},
		status_filter: function() {
			this.filter_tickets()
		}
	},
	computed: {
		tickets_reverse: function() {
			return this.tickets.slice().reverse()
		},

		tickets_by_alpabet: function() {
			return this.tickets.slice().sort(function(a, b) {
				// return (a.id > b.id) ? 1 : ((b.id > a.id) ? -1 : 0);
				return a.user_id - b.user_id;
			});
		},
	}
}
</script>
