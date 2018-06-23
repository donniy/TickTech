<template>
    <router-link :to="base_url + ticket.id" class="list-ticket">
        <h5>{{ticket.title}}</h5>
        Status: {{ticket.status.name}} </br>
        Time: {{ticket.timestamp}}
    </router-link>
</template>

<script>
    export default {
        props: {
            ticket: Object,
            base_url: {
                type: String,
                default: "/ticket/"
            }
        },
        data: function () {
            return {}
        }
    }
</script>