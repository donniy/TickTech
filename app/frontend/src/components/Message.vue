<template>
    <div :class="'message' + (user.id == message.user_id ? ' text-right' : '')">
        <h4 class="message-sender">{{username}}</h4>
        <div class="material-card sum">
            <p class="message-text">
            {{message.text}}
            {{user.id}}
            {{message.user_id}}
            </p>
        </div>
    </div>
</template>

<script>
    export default {
        props: ['message', 'user'],
        computed: {
            username: function() {
                return this.user.id == this.message.user_id ? 'You' : this.message.user_id
            },
        },
        data: function() {
            return {};
        },
    }
</script>
