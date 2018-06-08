<template>
    <tr v-on:click="showTicket">
        <th>{{ticket.title}}</th>
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
          return {
          }
      },
      methods: {
        showTicket () {
          this.$parent.showModal = true
          this.$parent.ticketSum = this.ticket.id
        }
      },
  }

</script>
