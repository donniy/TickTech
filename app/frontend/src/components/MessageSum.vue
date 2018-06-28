<template>
    <div :class="'message' + (this.$user.get().id == message.user_id ? ' text-right' : '')">
        <h4 class="message-sender">{{username}}</h4>
        <div class="material-card sum">
            {{message.text}}
        </div>
    </div>
</template>

<script>
    export default {
        props: ['message', 'user'],
        computed: {
            /* 
             * If user is the sender on the message page replaces user name with 'You'
             */
            username: function () {
                return this.$user.get().id == this.message.user_id ? 'You:' : this.message.user_id
            },
        },
        data: function () {
            return {}
        },
    }
</script>