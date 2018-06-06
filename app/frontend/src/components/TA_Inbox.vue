<template>
    <div>
        <h1>Welkom {{TA.name}}</h1>


        <b-table striped hover :items="cases">
            <template slot="name" slot-scope="data">
                <a :href="`#${data.value.replace(/[^a-z]+/i,'-').toLowerCase()}`">
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
            cases: [{
                        id: 1, 
                        name: "Tom van de Looij", 
                        course: "Project Software Engineering", 
                        status: "Pending",
                        date: "06-06-2018"
                     },
                    {
                        id: 2, 
                        name: "Jarno Bakker", 
                        course: "Project Software Engineering", 
                        status: "Pending",
                        date: "06-06-2018"
                    },
                    {
                        id: 3, 
                        name: "Damian Frölich", 
                        course: "Project Software Engineering", 
                        status: "Pending",
                        date: "06-06-2018"
                    }],
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
            const path = '/api/ticket/all'
            axios.get(path)
            .then(response => {
                this.cases = response.data
            })
            .catch(error => {
                console.log(error)
            })
        },

        getTACases () {
            const path = '/api/ticket/ta/' + this.$route.params.ta_id
            axios.get(path)
            .then(response => {
                this.cases = response.data
            })
            .catch(error => {
                console.log(error)
            })
        }
    },
    mounted: function () {
        this.getTA()
        this.getAllCases()
    }
}

</script>