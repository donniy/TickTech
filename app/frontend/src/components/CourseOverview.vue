<template>
    <div class="container">
      <h1>Courses</h1>

      <!-- <div class="col-md-6">
        <ul class="list-group">
          <li class="list-group-item" v-for="course in courses" v-bind:key="course.id">
            <a v-bind:href="'/course/'+course.id">
              <div class="col-md-2 col-sm-2">
                {{course.id}}
              </div>
              <div class="col-md-10  col-sm-10">
                {{course.name}}
              </div>
              <div class="col-md-12  col-sm-12">
                {{course.description}}
              </div>
            </a>
          </li>
        </ul>
      </div> -->

      <course
          v-for="course in courses"
          v-bind:key="course.id"
          v-bind:course="course"
      ></course>

    </div>
</template>

<script>

//library for ajax requests
import axios from 'axios'
import Course from './Course.vue'

export default {
  data () {
    return {
      courses: [],
      status: 'not set'
    }
  },
  methods: {
    getCourses () {
      this.status = 'getting courses'
      axios.get('/api/courses')
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
    created () {
      this.status = 'created'
      this.getCourses()
    }
  },
  mounted: function () {
    this.created()
  },
  components: {
    'course': Course,
  }
}

</script>
