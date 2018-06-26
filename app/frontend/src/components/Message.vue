<!-- Message.vue shows the messages of a ticket. -->
<template>
    <div class="md-layout-item md-size-100" >
        <template v-if="message.type == 0">
            <div :class="'media message' + (user.id == message.user_id ? ' text-right pl-0 pr-1' : ' pr-0 pl-1')">
                <img v-if="message.user_id != user.id" class="md-elevation-5 mr-3 rounded-circle" :src="'https://via.placeholder.com/64x64/FFFFFF/BC0031?text=' + username.match(/\b(\w)/g).join('')"
                />
                <md-card class="media-body">
                    <md-card-header>
                        <h5 class="md-title message-sender">{{username}}</h5>
                    </md-card-header>

                    <md-card-content>
                        <p class="message-text">
                            {{message.text}}
                        </p>
                    </md-card-content>
                </md-card>

                <img v-if="message.user_id == user.id" class="md-elevation-5 ml-3 rounded-circle" :src="'https://via.placeholder.com/64x64/FFFFFF/BC0031?text=' + username.match(/\b(\w)/g).join('')"
                />
            </div>
        </template>
        <template v-else-if="message.type == 2">
            <div class="notification notification-closed">
                {{username}} closed this ticket.
            </div>
        </template>
        <template v-else>
            <div>
                {{username}} {{message.text}}
            </div>
        </template>
    </div>
</template>

<script>
    export default {
        props: ['message', 'user'],
        computed: {
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
        mounted: function () {
        }
    }
</script>
