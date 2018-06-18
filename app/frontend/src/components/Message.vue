<template>
    <div>
        <template v-if="message.type == 0">
            <div :class="'media p-1 message' + (user.id == message.user_id ? ' text-right' : '')">
                <img v-if="message.user_id != user.id" class="mr-3 rounded-circle" :src="'https://via.placeholder.com/64x64/FFFFFF/BC0031?text=' + username.match(/\b(\w)/g).join('')"
                />
                <div class="media-body material-card">
                    <h5 class="mt-0 mb-1 message-sender">{{username}}</h5>
                    <p class="message-text">
                        {{message.text}}
                    </p>
                </div>
                <img v-if="message.user_id == user.id" class="ml-3 rounded-circle" :src="'https://via.placeholder.com/64x64/FFFFFF/BC0031?text=' + username.match(/\b(\w)/g).join('')"
                />
            </div>
        </template>
        <template v-else-if="message.type == 2">
            <div class="notification notification-closed">
                {{username}} closed this ticket
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
            console.log("Creating a new message")
            console.log("message.type: " + this.message.type)
            console.log("message.user_id: " + this.message.user_id)
            console.log("message.user_name: " + this.message.user_name)
        }
    }
</script>