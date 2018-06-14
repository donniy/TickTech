<template>
<div>
  <h1>Welkom {{ta.name}}</h1>
  <course v-for="course in courses" v-bind:key="course.id" v-bind:course="course"></course>
</div>
</template>

<script>
import Course from './Course.vue'

export default {
    data() {
    		return {
    			  ta: {},
    			  courses: []

    		}
    },
    methods: {
    		getTA() {
    			  const path = '/api/user/' + this.$route.params.ta_id
    			  this.$ajax.get(path)
    				    .then(response => {
    					      this.ta = response.data.json_data
    					      console.log(this.ta)
    				    })
    				    .catch(error => {
    					      console.log(error)
    				    })
    		},
    		getTaCourses() {
    			  this.$ajax.get('/api/ta/' + this.$route.params.ta_id + '/courses')
    				    .then(response => {
    					      this.courses = response.data.json_data
    					      console.log(this.courses)
    				    }).catch(error => {
    					      console.log(error)
    				    })
    		},
    		created() {
    			  this.getTA()
    			  this.getTaCourses()
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
