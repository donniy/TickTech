<template>
    <div>
        <h1>Welkom {{ta.name}}</h1>


        <!-- <b-table striped hover :items="cases">
            <template slot="id" slot-scope="data">
                <a v-bind:href="'/ticket/'+data.value">
                {{data.value}}
                </a>
            </template>
        </b-table> -->
        <course
          v-for="course in courses"
          v-bind:key="course.id"
          v-bind:course="course"
        ></course>
    </div>
</template>

<script>

import axios from 'axios'
import Course from './Course.vue'

export default {
    data () {
        return {
            ta: {},
            cases: [],
            courses: []

        }
    },
    methods: {
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
            const path = '/api/ta'
            axios.get(path)
            .then(response => {
                this.cases = response.data
            })
            .catch(error => {
                console.log(error)
            })
        },
        getTaCourses () {
            axios.get('/api/ta/'+ this.$route.params.ta_id + '/courses')
            .then(response => {
                this.courses = response.data.json_data
                console.log(this.courses)
            }).catch(error => {
                console.log(error)
            })
        },
        created () {
            this.getTA()
            this.getAllCases()
            this.getTaCourses()
        }
    },
    mounted: function () {
        this.created()
    },
    components: {
        'course': Course,
    }
}

</script>
