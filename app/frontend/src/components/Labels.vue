<template>
    <div>
        <div>
            <section>
                <h1>{{course.title}} labels</h1>

                <div class="addLabelWrapper">
                    <input v-model="new_label_name" class="addLabelInput"></input>
                    <button v-on:click="createLabel" class="labelbutton btn">Add label</button>
                </div>

            </section>
        </div>

        <div class="labelContainer">
            <myLabel
               v-for="label in labels"
               v-bind:key="label.label_id"
               v-bind:label="label"
             ></myLabel>
        </div>
   </div>
</template>

<script>

import axios from 'axios'
import Ticket from './Ticket.vue'
import Label from './Label.vue'

const axios_csrf = axios.create({
  headers: {'X-CSRFToken': 'need_to_replace'}
});

export default {
    data () {
        return {
            status: 'not set',
            labels : [],
            course: null,
            new_label_name: ''
        }
    },
    methods: {
        getCourse () {
          this.status = 'getting course'
          const path = '/api/courses/' + this.$route.params.course_id
          axios.get(path)
          .then(response => {
            this.course = response.data.json_data
            this.status = 'Retrieved data'
            console.log(response.data.json_data)
            console.log(response)
          })
          .catch(error => {
            console.log(error)
            this.status = 'failed getting course'
          })
        },
        getLabels () {
            this.status = 'getting labels'
            const path = '/api/labels/' + this.$route.params.course_id
            axios.get(path)
            .then(response => {
                this.labels = response.data.json_list
                this.status = 'Retrieved data'
                console.log(response.data.json_list)
                console.log(response)
            })
            .catch(error => {
                console.log(error)
                this.status = 'failed getting tickets'
            })
        },
        createLabel() {
            this.status = 'creating labels'
            const path = '/api/labels/' + this.$route.params.course_id
            axios_csrf.post(path, {name: this.new_label_name})
            .then(response => {
                this.tickets = response.data.json_list
                this.status = 'Retrieved data'
                console.log(response.data.json_list)
                console.log(response)
                this.getLabels()
            })
            .catch(error => {
                console.log(error)
                this.status = 'failed getting tickets'
            })
        },
         created () {
            this.status = 'created'
            this.getCourse()
            this.getLabels()
        }
    },
        mounted: function () {
            this.created()
    },
    components: {
         'myLabel': Label
    }
}

</script>
