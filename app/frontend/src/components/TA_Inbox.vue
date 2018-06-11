<template>
    <div>
        <h1>Welkom {{ta.name}}</h1>

        <div class="text-center btn_group">
            <b-button-group size="lg">
                <b-button @click="toggle()" variant="danger">Show All</b-button>
                <b-button @click="toggle()" variant="danger">Show My</b-button>
            </b-button-group>
        </div>

        <cases v-if="showAll === true"
            v-for="item in cases_all"
            v-bind:key="item.id"
            v-bind:cases="item"
        ></cases>
        <cases v-else-if="showTA === true"
            v-for="item in cases_ta"
            v-bind:key="item.id"
            v-bind:cases="item"
        ></cases>
    </div>
</template>

<script>

import axios from 'axios'
import Cases from './Cases.vue'

export default {
    data () {
        return {
            ta: {"name": "Erik Kooistra"},
            cases_all: [],
            cases_ta: [],
            showAll: true,
            showTA: false

        }
    },
    methods: {
        toggle() {
            if (this.showAll === true) {
                this.showAll = false
                this.showTA = true
            } else {
                this.showAll = true
                this.showTA = false
            }
        },
        getTA () {
            const path = '/api/user/' + this.$route.params.ta_id
            axios.get(path)
            .then(response => {
                this.ta = response.data.json_data
                console.log(this.ta)
            })
            .catch(error => {
                console.log(error)
            })
        },

        getAllCases () {
            const path = '/api/ta/' + this.$route.params.ta_idinbox + '/inbox'
            axios.get(path)
            .then(response => {
                this.cases_all = response.data.json_data
                console.log(response.data.json_data)
            })
            .catch(error => {
                console.log(error)
            })
        },

        getTACases () {
            const path = '/api/ta/' + this.$route.params.ta_idinbox + '/my_inbox'
            axios.get(path)
            .then(response => {
                this.cases_ta = response.data.json_data
                console.log(response.data.json_data)
            })
            .catch(error => {
                console.log(error)
            })
        },

        created () {
            this.getTA()
            this.getAllCases()
            // this.getTaCourses()
        }
    },
    mounted: function () {
        this.created()
    },
    components: {
        'cases': Cases
    }
}

</script>

<style lang="scss" scoped>

.btn_group {
    margin: 15px;
}
</style>
