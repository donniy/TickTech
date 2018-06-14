<template>
    <div :class="'message'">
        <h4 class="message-sender">{{username}}:</h4>
        <div class="material-card sum-original">
            <h5 class="message-sender">{{message.title}}</h5>
            {{message.text}}
        </div>
        <p>{{message.time}}</p>
    </div>
</template>

<script>
    export default {
        props: ['message', 'user'],
        computed: {
            username: function() {
                return this.$user.get().name
            },
        },
        data: function() {
            return {};
        },
    }
</script>
