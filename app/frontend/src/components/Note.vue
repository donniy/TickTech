<template>
    <div class="material-card note">
        <h4>{{note.user_id}}:</h4>
        <p>
            {{note.text}}
        </p>
    </div>
</template>

<script>

  export default {
      props: ['note'],
      data: function () {
          return {};
      }
  }

</script>
