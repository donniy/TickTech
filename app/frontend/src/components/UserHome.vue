<template>
    <div class="container">
        <div class="md-layout welcome-header">
            <h2>Welcome back {{ $user.get().name }}</h2>
        </div>
        <div class="md-layout md-gutter wrapper">
            <div class="md-layout-item" v-if="isTA">
                <md-content class="md-elevation-5">
                        <md-subheader>Courses</md-subheader>

                        <md-content class="md-scrollbar courses-section">
                        <md-list class="md-triple-line">

                            <course v-for="course in courses" v-bind:key="course.id" v-bind:course="course"></course>

                        </md-list>
                        </md-content>

                </md-content>
            </div>
            <div class="md-layout-item" v-if="!isTA">
                <md-content class="md-elevation-5">
                        <md-subheader>Tickets</md-subheader>

                        <md-content class="md-scrollbar courses-section">
                        <md-list class="md-triple-line">

                            <course v-for="ticket in tickets" v-bind:key="ticket.title" v-bind:course="ticket"></course>

                        </md-list>
                        </md-content>

                </md-content>
            </div>
            <div class="md-layout-item">
                <md-content class="md-elevation-5">
                    <md-list class="md-double-line padding-bottom-0">
                        <md-subheader>Notifications</md-subheader>

                        <md-content class="md-scrollbar notification-section">
                            <p style="padding-left: 16px;" v-if="tickets.length < 1">No notifications</p>
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

                                <md-divider></md-divider>
                            </template>
                        </md-content>

                    </md-list>
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

    export default {
        data() {
            return {
                courses: [],
                status: 'not set',
                tickets: [],
                isTA: false,
                notifications: [],
            }
        },
        methods: {
            getTickets() {
				this.status = 'getting tickets'
				const path = '/api/user/' + this.$user.get().id + '/tickets'
				this.$ajax.get(path).then(response => {
					this.tickets = response.data.json_data
				}).catch(error => {
					console.log(error)
				})
			},
            getCourses() {
                let courses_ta_in = Object.keys(this.$user.get().ta).length
                if (courses_ta_in == 0) {
                    this.courses = [];
                    this.isTA = false;
                    return;
                }
                this.status = 'getting courses'
                this.courses = [this.$user.get().ta]
                this.isTA = true;
            },

            getTodos () {
                this.$ajax.get('/api/user/notifications', response => {
                    console.log(response.data.json_data)
                    this.notifications = response.data.json_data
                })
            },
            created() {
                this.status = 'created'
                this.getCourses()
                this.getTodos()
                this.getTickets()
            }
        },
        mounted: function () {
            this.created()

            if (!this.$user.logged_in()) {
                this.$router.push('/login')
            }
        },
        components: {
            'course': Course,
        }
    }
</script>
