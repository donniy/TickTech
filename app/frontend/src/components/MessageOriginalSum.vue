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
            /* 
             * If user is the sender on the message page replaces user name with 'You'
             */
            username: function () {
                if (this.user) {
                    return this.user.id == this.message.user_id ? 'You' : this.message.user_name
                } else {

                    return 'unknown'
                }
            },
        },
        data: function () {
            return {}
        },
    }
</script>