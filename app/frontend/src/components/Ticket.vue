<template>
    <a v-bind:href="'/ticket/' + ticket.id" class="list-ticket">
        <h3>{{ticket.title}}</h3>
        Status: {{ticket.status.name}} - Gesteld door: {{ticket.user_id}}
    </a>
</template>

<script>

  export default {
      props: ['ticket'],
      data: function () {
          return {};
      }
  }

</script>
