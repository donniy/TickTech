<template>
    <div class="container">
        <div class="row">
            <div class="col-lg-12">
                <h2 style="text-align:center;">Welcome back {{ $user.get().name }} :)</h2>
                <br />
                <hr style="width: 20%;">
                <br />
            </div>
            <div class="col-lg-8 text-center">
                <h5>Notifications</h5>
                <div class="notification-container">
                    <p v-if="tickets.length < 1">- No notifications -</p>
                    <ticket v-for="ticket in tickets" v-bind:key="ticket.id" v-bind:ticket="ticket" v-bind:base_url="'/student/ticket/'"></ticket>
                </div>
                <router-link style="float:right;" to="/settings">Settings</router-link>
                <router-link style="float:right;" to="/ticket/submit">Create ticket</router-link>
                <router-link style="float:right;" to="/user/tickets">All tickets</router-link>
            </div>
            <div class="col-lg-4 text-center" v-if="isTA">
                <h5>TA Courses</h5>
                <div class="home-scroll-courses">
                  <course v-for="course in courses"
                          v-bind:key="course.id"
                          v-bind:course="course">
                  </course>
                </div>
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
            }
        },
        methods: {
            getCourses() {
                let courses_ta_in = Object.keys(this.$user.get().ta).length
                console.log(courses_ta_in)
                if (courses_ta_in == 0) {
                    this.courses = [];
                    this.isTA = false;
                    return;
                }
                this.status = 'getting courses'
                /* We now get the ta courses from the user object.
                   Students only dont have courses
                this.$ajax.get('/api/courses')
                    .then(response => {
                        //this.courses = response.data.json_data
                        this.status = 'Retrieved data'
                        console.log(response)
                    })
                    .catch(error => {
                        console.log(error)
                        this.status = 'failed getting courses'
                    })
                */
                this.courses = [this.$user.get().ta]
                this.isTA = true;
            },
            created() {
                this.status = 'created'
                this.getCourses()
                this.$ajax.get('/api/user/notifications', (response) => {
                    console.log(response.data.json_data)
                })
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
