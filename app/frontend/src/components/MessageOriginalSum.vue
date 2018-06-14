<template>
    <div :class="'message'">
        <h4 class="message-sender">{{username}}:</h4>
        <div class="material-card sum-original">
            <h5 class="message-sender">{{this.message.title}}</h5>
            {{this.message.text}}
        </div>
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
