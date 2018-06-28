<template>
    <div>
        <h2 class="form-header center-display">labels in {{course.title}}</h2>
        <form class="md-layout center-display" v-on:submit.prevent="createLabel">
            <md-card class="center-display md-layout-item md-size-50 md-small-size-100">
                <md-card-content class="center-display">
                    <md-field class="center-display md-layout-item md-size-100">
                        <label for="labelname">New label</label>
                        <md-input id="labelname" name="labelname" v-validate="'required|max:50'" v-model="new_label_name" />
                        <md-button type="submit" v-bind:disabled="errors.any()">
                            Submit
                        </md-button>
                    </md-field>
                </md-card-content>
            </md-card>
        </form>
        </br>

        <div class="md-layout md-gutter">
            <div class="md-layout-item">
                <md-content class="md-elevation-3">
                    <md-list>
                        <md-subheader>Edit labels</md-subheader>
                        <my-label @label-selected="selected_label = label" v-for="label in labels" v-bind:key="label.label_id" v-bind:label="label"></my-label>
                    </md-list>
                </md-content>
            </div>
            <div class="md-layout-item">
                <md-content class="md-elevation-3">
                    <md-list class="md-double-line md-dense">
                        <label-details @label-deselected="selected_label = null" v-if="selected_label" :label="selected_label" />
                        <md-empty-state
                                   v-else
                                   md-rounded
                                   md-icon="label"
                                   md-label="No label selected"
                                   md-description="Click a label on the left to edit its properties." />
                        </md-empty-state>
                    </md-list>
                </md-content>
            </div>
        </div>
    </div>
</template>

<script>
import Ticket from './Ticket.vue'
import Label from './Label.vue'
import LabelDetails from './LabelDetails.vue'

export default {
    data() {
        return {
            course: { title: "loading" },
            labels: [],
            selected_label: null,
            new_label_name: ''
        }
    },
    methods: {
        // Retrieve current course.
        getCourse() {
            const path = '/api/courses/single/' + this.$route.params.course_id
            this.$ajax.get(path, response => {
                this.course = response.data.json_data
            })
        },
<<<<<<< HEAD
        // Retrieve all labels associated with current course.
        getLabels() {
            const path = '/api/labels/' + this.$route.params.course_id
            this.$ajax.get(path, response => {
                this.labels = response.data.json_data
            })
=======
        methods: {
            /* 
             * Get all info from a course.
             */
            getCourse() {
                const path = '/api/courses/single/' + this.$route.params.course_id
                this.$ajax.get(path).then(response => {
                    this.course = response.data.json_data
                }).catch(error => {
                    console.log(error)
                    this.$router.go(-1)
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
>>>>>>> master
        },
        // Add a new label.
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
    // This is done when the page is loaded.
    mounted: function () {
        if (!this.$user.logged_in()) {
            this.$router.push('/login')
        }
        this.getCourse()
        this.getLabels()
    },
    components: {
        'my-label': Label,
        'label-details': LabelDetails,
    }
}
</script>
