<template>
    <div class="container">
        <div class="md-layout welcome-header">
            <h2>Welcome back {{ $user.get().name }} :)</h2>
        </div>
        <div class="md-layout md-gutter wrapper">
            <!-- <div class="md-layout-item">
                <md-content class="md-scrollbar notification-section">
                    <div class="md-list-item-text">
                        <course v-for="course in courses" v-bind:key="course.id" v-bind:course="course"></course>
                    </div>
                </md-content> -->
                <div class="md-layout-item">
                    <md-content class="md-elevation-5">
                        <md-list class="md-double-line">
                            <md-subheader>Courses</md-subheader>

                            <md-content class="md-scrollbar courses-section">

                                <course v-for="course in courses" v-bind:key="course.id" v-bind:course="course" class="md-list-item-text single-course"></course>

                            </md-content>

                        </md-list>
                    </md-content>
            </div>
            <div class="md-layout-item">
                <md-content class="md-elevation-5">
                    <md-list class="md-double-line">
                        <md-subheader>Notifications</md-subheader>

                        <md-content class="md-scrollbar notification-section">
                            <md-ripple>
                                <md-list-item to="/asdf">
                                    <div class="md-list-item-text">
                                        <span>Erik Kooistra</span>
                                        <span>Je krijgt geen hoger cijfer</span>
                                    </div>
                                </md-list-item>
                            </md-ripple>

                            <md-divider></md-divider>

                            <md-list-item to="/asdf">
                                <div class="md-list-item-text">
                                    <span>Erik Kooistra</span>
                                    <span>Je krijgt geen hoger cijfer</span>
                                </div>
                            </md-list-item>

                            <md-divider></md-divider>

                            <md-list-item to="/asdf">
                                <div class="md-list-item-text">
                                    <span>Erik Kooistra</span>
                                    <span>Je krijgt geen hoger cijfer</span>
                                </div>
                            </md-list-item>

                            <md-divider></md-divider>

                            <md-list-item to="/asdf">
                                <div class="md-list-item-text">
                                    <span>Erik Kooistra</span>
                                    <span>Je krijgt geen hoger cijfer</span>
                                </div>
                            </md-list-item>

                            <md-divider></md-divider>

                            <md-list-item to="/asdf">
                                <div class="md-list-item-text">
                                    <span>Erik Kooistra</span>
                                    <span>Je krijgt geen hoger cijfer</span>
                                </div>
                            </md-list-item>

                            <md-divider></md-divider>

                            <md-list-item to="/asdf">
                                <div class="md-list-item-text">
                                    <span>Erik Kooistra</span>
                                    <span>Je krijgt geen hoger cijfer</span>
                                </div>
                            </md-list-item>

                            <md-divider></md-divider>

                            <md-list-item to="/asdf">
                                <div class="md-list-item-text">
                                    <span>Erik Kooistra</span>
                                    <span>Je krijgt geen hoger cijfer</span>
                                </div>
                            </md-list-item>

                            <md-divider></md-divider>

                            <md-list-item to="/asdf">
                                <div class="md-list-item-text">
                                    <span>Erik Kooistra</span>
                                    <span>Je krijgt geen hoger cijfer</span>
                                </div>
                            </md-list-item>
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
                tickets: []
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
            created() {
                this.status = 'created'
                this.getCourses()
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
