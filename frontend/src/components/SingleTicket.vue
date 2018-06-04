<template>
    <div>
        <h1>{{ticket.title}}</h1>
        <h2>Gebruiker: {{ticket.user_id}}</h2>
        Status: {{ticket.status.name}}
    </div>
</template>

<script>

import axios from 'axios'

export default {
    data () {
        return {
            ticket: {},
        }
    },
    methods: {
        getTicket () {
            const path = '/api/ticket/' + this.$route.params.ticket_id
            axios.get(path)
            .then(response => {
                this.ticket = response.data
            })
            .catch(error => {
                console.log(error)
            })
        },
    },
    mounted: function () {
        this.getTicket()
    }
}

</script>
