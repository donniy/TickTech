<template>
    <div class="container">
        <div class="md-layout welcome-header">
            <h2>Welcome back {{ $user.get().name }} :)</h2>
        </div>
        <div class="md-layout md-gutter wrapper">
            <div class="md-layout-item">
                <md-content class="md-elevation-5">
                        <md-subheader>Courses</md-subheader>

                        <md-content class="md-scrollbar courses-section">
                        <md-list class="md-triple-line">

                            <course v-for="course in courses" v-bind:key="course.id" v-bind:course="course"></course>
                        
                        </md-list>
                        </md-content>

                </md-content>
            </div>
            <div class="md-layout-item">
                <md-content class="md-elevation-5">
                    <md-list class="md-double-line">
                        <md-subheader>Notifications</md-subheader>

                        <md-content class="md-scrollbar notification-section">
                            <template v-for="notification in notifications">
                                <md-ripple>
                                    <md-list-item :to="{name: (notification.ta ? 'SingleTicket' : 'StudentTicket'), params: {ticket_id: notification.ticket.id}}">
                                        <div class="md-list-item-text">
                                            <span>{{notification.ticket.title}}</span>
                                            <span>Je krijgt geen hoger cijfer</span>
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
                            <h1>Create ticket</h1>
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
                notifications: [],
            }
        },
        methods: {
            getCourses() {
                this.status = 'getting courses'
                this.$ajax.get('/api/courses')
                    .then(response => {
                        this.courses = response.data.json_data
                        this.status = 'Retrieved data'
                        console.log(response)
                    })
                    .catch(error => {
                        console.log(error)
                        this.status = 'failed getting courses'
                    })
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
