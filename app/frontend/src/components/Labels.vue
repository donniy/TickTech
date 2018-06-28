<template>
    <div>
    <h2 class="form-header center-display">labels in {{course.title}}</h2>
    <form class="md-layout center-display" v-on:submit.prevent="createLabel">
        <md-card class="center-display md-layout-item md-size-50 md-small-size-100">
            <md-card-content class="center-display">
                <md-field class="center-display md-layout-item md-size-100">
                    <label for="labelname">New label</label>
                    <md-input id="labelname" name="labelname" v-validate="'required|max:50'" v-model="new_label_name"/>
                    <md-button type="submit" v-bind:disabled="errors.any()">
                        Submit
                    </md-button>
                </md-field>
            </md-card-content>
        </md-card>
    </form>
    </br>
    <p class="md-helper-text center-display">Select labels you want to be bound to.</p>

    <div class="md-layout center-display">
        <md-card class="center-display md-layout-item md-size-50 md-small-size-100">
            <md-card-content>
                <myLabel v-for="label in labels" v-bind:key="label.label_id" v-bind:label="label"></myLabel>
            </md-card-content>
        </md-card>
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
            /* 
             * Get all info from a course.
             */
            getCourse() {
                const path = '/api/courses/single/' + this.$route.params.course_id
                this.$ajax.get(path, response => {
                    this.course = response.data.json_data
                })
            },
            /*
             * Get all labels in a coures.
             */
            getLabels() {
                const path = '/api/labels/' + this.$route.params.course_id
                this.$ajax.get(path, response => {
                    this.labels = response.data.json_data
                })
            },
            /*
             * Insert new label to the list of labels in a course.
             */
            createLabel() {
                if (this.new_label_name == '') {
                    return
                }
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
