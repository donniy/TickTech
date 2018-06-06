<template>
    <div :class="'message' + (self == message.user_id ? ' text-right' : '')">
        <h4>{{message.user_id}}</h4>
        <div class="material-card">
            {{message.text}}
        </div>
    </div>
</template>

<script>

  export default {
      props: ['message', 'self'],
      data: function () {
          return {};
      }
  }

</script>
