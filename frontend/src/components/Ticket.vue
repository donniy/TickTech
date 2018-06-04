<template>
    <div>
        <h2><a v-bind:href="'/ticket/' + ticket.id">{{ticket.user_id}}: {{ticket.title}}</a></h2>
    </div>
</template>

<script>

  export default {
      props: ['ticket'],
      data: function () {
          return {};
      }
  }

</script>
