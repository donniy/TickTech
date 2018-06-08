<template>
    <div :class="'message' + (self == message.user_id ? ' text-right' : '')">
        <h4>{{username}}</h4>
        <div class="material-card">
            {{message.text}}
        </div>
    </div>
</template>

<script>

export default {
    props: ['message', 'self'],
    computed: {
        username: function () {
            return this.self == this.message.user_id ? 'You' : this.message.user_id
        },
    },
    data: function () {
        return {};
    }
}

</script>
