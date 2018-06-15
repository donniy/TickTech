<template>
    <div class="container">
        <div class="row">
            <div class="col-lg-12">
                <h2 style="text-align:center;">Homepage for {{ $user.get().name }}</h2>
            </br>
                <hr style="width: 20%;">
            </br>
            </div>
            <div class="col-lg-8 text-center">
                <h5>Notifications</h5>
                <div class="notification-container">
                    <p v-if="tickets.length < 1">- No notifications -</p>
                    <ticket
                    v-for="ticket in tickets"
                    v-bind:key="ticket.id"
                    v-bind:ticket="ticket"
                    v-bind:base_url="'/student/ticket/'"
                    ></ticket>
                </div>
                <router-link style="float:right;"to="/settings">Settings</router-link>
                <router-link style="float:right;"to="/form">Create ticket</router-link>
            </div>
            <div class="col-lg-4 text-center" >
                <h5>Courses</h5>
                <div class="home-scroll-courses">
                    <course v-for="course in courses" v-bind:key="course.id" v-bind:course="course"></course>
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
      mounted: function() {
        this.created()
      },
      components: {
        'course': Course,
      }
    }
</script>
