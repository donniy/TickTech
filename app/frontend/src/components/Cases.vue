<template>
    <a v-bind:href="'/ticket/'+cases.id" class="list-ticket">
        <h3>{{cases.title}}</h3>
        {{cases.email}} {{cases.timestamp}} {{cases.user_id}}
    </a>
</template>

<script>

  export default {
      props: ['cases'],
      data: function () {
          return {};
      }
  }

</script>