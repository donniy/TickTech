<template>
    <router-link class="ticket-single" :to="base_url + ticket.id">
      <md-ripple>
    	  <h6>{{ticket.title}}</h6>
        In course: {{ this.course }}</br>
        Status: {{ticket.status.name}} </br>
        Time: {{ticket.timestamp}}
    </md-ripple>
    </router-link>
</template>

<script>

export default {
		props: {
			  ticket: Object,
 			  base_url: {
				    type: String,
				    default: "/student/ticket/"
			  },
        TA_view: false,
		},
		data: function () {
			  return {
            course: ''
        }
		}, methods: {
        getCourse() {
                const path = '/api/courses/single/' + this.ticket.course_id
                this.$ajax.get(path, response => {
                    this.course = response.data.json_data['title']
                })
            }
    }, mounted() {
        if (this.TA_view) {
            this.base_url = '/ticket/'
        }

        this.getCourse()
        }
    }
</script>
