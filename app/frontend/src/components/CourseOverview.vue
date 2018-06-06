<template>
    <div>
        <h1>Courses</h1>
        <ul>
          <li v-for="course in courses"
              v-bind:key="course.id"
              v-bind:course="course">
          </li>
        </ul>
    </div>
</template>

<script>

//library for ajax requests
import axios from 'axios'

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
      const path = '/api/courses'
      axios.get(path)
      .then(response => {
        this.courses = response.data.json_list
        this.status = 'Retrieved data'
        console.log(response.data.json_list)
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
  }
}

</script>
