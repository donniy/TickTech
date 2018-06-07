<template>
    <div>
        <h1>Welkom {{TA.name}}</h1>


        <b-table striped hover :items="cases">
            <template slot="id" slot-scope="data">
              <a v-bind:href="'/ticket/'+data.value">
                  {{data.value}}
              </a>
            </template>
        </b-table>
    </div>
</template>

<script>

import axios from 'axios'

export default {
    data () {
        return {
            TA: {name: "Erik Kooistra"},
            cases: [],

        }
    },
    methods: {
        getTA () {
            const path = '/api/ta/' + this.$route.params.ta_id
            axios.get(path)
            .then(response => {
                this.ta = response.data
            })
            .catch(error => {
                console.log(error)
            })
        },

        getAllCases () {
            const path = '/api/ta'
            axios.get(path)
            .then(response => {
                this.cases = response.data
            })
            .catch(error => {
                console.log(error)
            })
        },
        created () {
            this.getAllCases()
        }
    },
    mounted: function () {
        this.created()
    }
}

</script>
