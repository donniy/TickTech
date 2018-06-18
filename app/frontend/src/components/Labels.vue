<template>
    <div>

        <div>
            <h1>{{course.title}} labels</h1>

            <div class="addLabelWrapper">
                <input v-model="new_label_name" class="addLabelInput" />
                <button v-on:click="createLabel" class="labelbutton btn">Add label</button>
            </div>
        </div>


        <div class="labelContainer">
            <myLabel v-for="label in labels" v-bind:key="label.label_id" v-bind:label="label"></myLabel>
        </div>
    </div>
</template>

<script>
    import Ticket from './Ticket.vue'
    import Label from './Label.vue'

    export default {
        data() {
            return {
                course: { title: "loading" },
                labels: [],
                new_label_name: ''
            }
        },
        methods: {
            getCourse() {
                const path = '/api/courses/single/' + this.$route.params.course_id
                this.$ajax.get(path, response => {
                    this.course = response.data.json_data
                })
            },
            getLabels() {
                const path = '/api/labels/' + this.$route.params.course_id
                this.$ajax.get(path, response => {
                    this.labels = response.data.json_data
                })
            },
            createLabel() {
                const path = '/api/labels/' + this.$route.params.course_id
                this.$ajax.post(path, {
                    name: this.new_label_name
                }, response => {
                    this.tickets = response.data.json_data
                    this.new_label_name = ''
                    this.getLabels()
                })
            }
        },
        mounted: function () {
            if (!this.$user.logged_in()) {
                this.$router.push('/login')
            }
            this.getCourse()
            this.getLabels()
        },
        components: {
            'myLabel': Label
        }
    }
</script>