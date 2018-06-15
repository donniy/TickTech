<template>
<div>
  <user v-for="user in users" v-bind:user="user">
    </user>
  </div>

</template>

<script>
import User from './User.vue'

export default {
    data () {
        return {
            users: []
        }
    },
    components: {
        'user': User,
    },
    methods: {
        getUsers() {
            console.log(this.$route.params.course_id)
        }
    },
    mounted: function (){
        const path = '/api/courses/' + this.$route.params.course_id + '/tas'
        this.$ajax.get(path)
            .then(response => {
                this.users = response.data.json_data
                console.log(this.users)
            })
        this.getUsers()
    },

}

</script>
