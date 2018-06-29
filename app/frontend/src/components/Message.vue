<template>
    <div v-if="$auth.ready()" class="md-layout-item md-size-100" >
        <template v-if="message.type == 0">
            <div :class="'media message' + (user.id == message.user_id ? ' text-right pl-0 pr-1' : ' pr-0 pl-1')">
                <img v-if="message.user_id != user.id" class="md-elevation-5 mr-3 rounded-circle" :src="'https://via.placeholder.com/64x64/FFFFFF/BC0031?text=' + username.match(/\b(\w)/g).join('')"
                />
                <md-card class="media-body">
                    <md-card-header>
                        <h5 class="md-title message-sender">{{username}}
                            <p v-if="username === ta_name" v-for="(ta_name, key) in ta_names" v-bind:key="key" class="ranktext" id="ranking">
                                {{rank}}
                            </p>
                            <p v-if="(username === 'You' && $auth.check('ta'))" class="ranktext" id="ranking">
                                {{rank}}
                            </p>
                        </h5>
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
        <template v-else-if="message.type == 4 || message.type == 5">
            <div class="md-subhead">
                <p class="center-display">{{username}} {{message.text}}</p>
            </div>
        </template>
        <template v-else-if="message.type == 8">
            <div class="md-subhead">
                <p class="center-display">{{username}} got assigned this ticket.</p>
            </div>
        </template>
    </div>
</template>

<script>
export default {
    data() {
        return {
            level: 0,
            rank: '',
            ta_names: []
        }
    },
    props: ['message', 'user', 'tas'],
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
    methods: {
        /*
         * Get the current level of a user from the database.
         */
        getLevel() {
            const path = '/api/user/getsinglelevel/' + this.message.user_id
			this.$ajax.get(path).then(response => {
                this.level = response.data.json_data.level
                this.getRanking()

                for(let i = 0; i < this.tas.length; i++) {
                    let ta = this.tas[i]
                    this.ta_names.push(ta.name)
                }

			}).catch(error => {
				console.log(error)
			})
        },
        /*
         * Display corresponding rank with the current level of the user.
         */
        getRanking() {
            if (this.level) {
                if (this.level < 5) {
                    this.rank = "Novice TA (" + this.level + ")"
                } else if (this.level < 10) {
                    this.rank = "Adept TA (" + this.level + ")"
                } else if (this.level < 15) {
                    this.rank = "Advancing TA (" + this.level + ")"
                } else if (this.level < 18) {
                    this.rank = "Advanced TA (" + this.level + ")"
                } else if (this.level < 23) {
                    this.rank = "Advanced'st TA (" + this.level + ")"
                } else if (this.level < 28) {
                    this.rank = "Advanced'st've TA (" + this.level + ")"
                } else if (this.level < 30) {
                    this.rank = "Powerfull TA (" + this.level + ")"
                } else if (this.level < 38) {
                    this.rank = "Dr. TikTech (" + this.level + ")"
                } else if (this.level < 45) {
                    this.rank = "No-lifer (" + this.level + ")"
                } else if (this.level < 55) {
                    this.rank = "Question master (" + this.level + ")"
                } else if (this.level < 60) {
                    this.rank = "Dr. Prof. TikTech (" + this.level + ")"
                } else if (this.level < 65) {
                    this.rank = "TA Lord (" + this.level + ")"
                } else if (this.level < 70) {
                    this.rank = "Teaching Elder (" + this.level + ")"
                } else if (this.level < 75) {
                    this.rank = "TikTechian (" + this.level + ")"
                } else if (this.level < 85) {
                    this.rank = "Mega-TikTechian (" + this.level + ")"
                } else if (this.level < 90) {
                    this.rank = "Super-Mega-TikTechian (" + this.level + ")"
                } else if (this.level < 95) {
                    this.rank = "The Oracle (" + this.level + ")"
                } else if (this.level < 99) {
                    this.rank = "The One who Answers (" + this.level + ")"
                } else {
                    this.rank = "Master of TikTech (" + this.level + ")"
                }
            }
        }
    },
    mounted: function() {
        this.getLevel()
    }
}
</script>
