<template>
    <div class="md-layout-item md-size-100" >
        <template v-if="message.type == 0">
            <div :class="'media message' + (user.id == message.user_id ? ' text-right pl-0 pr-1' : ' pr-0 pl-1')">
                <img v-if="message.user_id != user.id" class="md-elevation-5 mr-3 rounded-circle" :src="'https://via.placeholder.com/64x64/FFFFFF/BC0031?text=' + username.match(/\b(\w)/g).join('')"
                />
                <md-card class="media-body">
                    <md-card-header>
                        <h5 class="md-title message-sender">{{username}} - {{rank}}</h5>
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
                {{username}} closed this ticket
            </div>
        </template>
        <template v-else-if="message.type != 7 && message.type != 6">
            <div class="md-subhead">
                <p class="center-display">{{username}} {{message.text}}</p>
            </div>
        </template>
    </div>
</template>

<script>
export default {
    data() {
        return {
            level: 0
        }
    },
    props: ['message', 'user'],
    computed: {
        username: function () {
            if (this.user) {
                return this.user.id == this.message.user_id ? 'You' : this.message.user_name
            } else {

                return 'unknown'
            }
        },
        rank: function () {
            if (this.level) {
                if (this.level < 5) {
                    return "Novice TA (" + this.level + ")"
                } else if (this.level < 10) {
                    return "Adept TA (" + this.level + ")"
                } else if (this.level < 15) {
                    return "Advancing TA (" + this.level + ")"
                } else if (this.level < 18) {
                    return "Advanced TA (" + this.level + ")"
                } else if (this.level < 23) {
                    return "Advanced'st TA (" + this.level + ")"
                } else if (this.level < 28) {
                    return "Advanced'st've(" + this.level + ")"
                } else if (this.level < 30) {
                    return "Powerfull TA (" + this.level + ")"
                } else if (this.level < 38) {
                    return "Dr. TikTech (" + this.level + ")"
                } else if (this.level < 45) {
                    return "No-lifer (" + this.level + ")"
                } else if (this.level < 55) {
                    return "Question master (" + this.level + ")"
                } else if (this.level < 60) {
                    return "Dr. Prof. TikTech (" + this.level + ")"
                } else if (this.level < 65) {
                    return "TA Lord (" + this.level + ")"
                } else if (this.level < 70) {
                    return "Teaching Elder (" + this.level + ")"
                } else if (this.level < 75) {
                    return "TikTechian (" + this.level + ")"
                } else if (this.level < 85) {
                    return "Mega-TikTechian (" + this.level + ")"
                } else if (this.level < 90) {
                    return "Super-Mega-TikTechian (" + this.level + ")"
                } else if (this.level < 95) {
                    return "The Oracle (" + this.level + ")"
                } else if (this.level < 99) {
                    return "The One who Answers (" + this.level + ")"
                } else {
                    return "Master of TikTech (" + this.level + ")"
                }
            }
        },
    },
    methods: {
        getLevel() {
            const path = '/api/user/getsinglelevel/' + this.user.id
			this.$ajax.get(path).then(response => {
				this.level = response.data.json_data['level']
                console.log(this.level)
			}).catch(error => {
				console.log(error)
			})
        },
    },
    created: function () {
        this.getLevel()
    }
}
</script>
