<template>
    <div class="material-card message">
        <h4>{{message.user_id}}:</h4>
        <p>
            {{message.text}}
        </p>
    </div>
</template>

<script>

  export default {
      props: ['message'],
      data: function () {
          return {};
      }
  }

</script>
