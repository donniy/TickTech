<template>
    <div :class="'message' + (this.$user.get().id == note.user_id ? ' text-right' : '')">
        <h4 class="message-sender">{{note.user_id}}:</h4>
        <div class="material-card sum">
            {{note.text}}
        </div>
    </div>
</template>


<script>


  export default {
      props: ['note'],
      data: function () {
          return {
          };
      }
  }

</script>
