<template>
  <div>
    name: {{ user.name }} student id: {{ user.user_id }} email: {{ user.email }}
  </div>
</template>


<script>
export default {
    props: ['user']

}

</script>
