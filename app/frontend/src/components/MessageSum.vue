<template>
    <div :class="'messagesum' + (self == message.user_id ? ' text-right' : '')">
        <h5>{{message.user_id}}</h5>
        <div class="material-card sum">
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

<style>
.sum {
  width: 90%;
  word-wrap: break-word;
}
</style>