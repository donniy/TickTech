<template>
    <tr v-on:mouseover="showTicket" v-on:click="navTicket" style="cursor:pointer;" class="singleTicket">
        <th>{{ticket.title}}</th>
        <td>{{ticket.label.label_name}}</td>
        <td>{{ticket.user_id}}</td>
        <td>{{ticket.status.name}}</td>
        <td>{{ticket.timestamp}}</td>
    </tr>
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
        },
        methods: {
            showTicket() {
                this.$parent.showSum = true
                this.$parent.ticketSum = this.ticket.id
            },
            navTicket() {
                this.$router.push("/ticket/" + this.ticket.id)
            }
        },
    }
</script>