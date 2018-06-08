<template>
    <div :class="'message' + (user.user_id == message.user_id ? ' text-right' : '')">
        <h4>{{username}}</h4>
        <div class="material-card">
            {{message.text}}
        </div>
    </div>
</template>

<script>

export default {
    props: ['message', 'user'],
    computed: {
        username: function () {
            return this.user.user_id == this.message.user_id ? 'You' : this.message.user_id
        },
    },
    data: function () {
        return {};
    },
}

</script>
