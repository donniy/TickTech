<template>
    <div>
        <!--Student name and number  -->
        <div class="row justify-content-around">
            <div class="col-sm-8 col-md-6">
                    <h2 class="form-header">Submit a question</h2>
                <form class="material-form" v-on:submit.prevent="sendTicket">
                    <div class="form-group">
                        <label for="subject">Subject</label>
                        <input id="subject" class="form-control" v-validate="'required|max:50'" name="subject" v-model="form.subject" type="text" placeholder="Question about...">
                        <div v-show="errors.has('subject')" class="invalid-feedback">
                            {{ errors.first('subject') }}
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="message">Message</label>
                        <textarea-autosize id="message" class="form-control" name="message" v-validate="'required'" placeholder="While working at the assignment, I ran into..." v-model="form.message"></textarea-autosize>
                        <div v-if="errors.has('message')" class="invalid-feedback">
                            {{ errors.first('message') }}
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="course">Course</label>
                        <select id="course" v-validate="''" class="form-control custom-select" v-model="form.courseid">
                            <option disabled value="">Please select a course</option>
                            <option v-for="obj in categories.courses" v-bind:value="obj.id">
                            {{ obj.title }}
                            </option>
                        </select>

                    </div>
                    <div class="form-group">
                        <label for="category">Category</label>
                        <select id="category" v-validate="''" class="form-control custom-select" v-model="form.labelid">
                            <option disabled value="">Label this question</option>
                            <option v-for="option in categories.labels[form.courseid]" v-bind:value="option.label_id">{{ option.label_name }}</option>
                        </select>
                        <small class="form-text">Selecting a category is optional, but can help assign your question to the right person.</small>

                    </div>

                    <button type="submit" class="btn btn-primary btn-block btn-lg" v-bind:disabled="errors.any()">
                        Submit
                    </button>

                    <p class="def-error-msg" v-show="errors.any()">
                    Please fill out the form correctly
                    </p>

                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import VeeValidate from 'vee-validate';

export default {
    data() {
        return {
            form: {
                name: "",
                studentid: "",
                email: "",
                message: "",
                courseid: "",
                labelid: "",
                subject: "",
            },
            categories: {
                courses: [],
                labels: {}
            }
        }
    },
    computed: {
        options: function(event) {
            return categories.labels[form.courseid]
        }
    },
    methods: {
        sendTicket() {
            this.$validator.validateAll()
            const path = '/api/ticket/submit'
            this.$ajax.post(path, this.form)
                .then(response => {
                    this.$router.push({
                        name: 'StudentTicket',
                        params: {
                            ticket_id: response.data.json_data.ticketid
                        }
                    })

                    console.log("Pushed")
                    this.form = ""
                }).catch(error => {
                    console.log(error)
                })
        },
        onChange: function(e) {
            this.categories = this.categories
        },
        mounted: function() {

        }
    },
    mounted() {
        const pathLabels = '/api/labels';
        const pathCourses = '/api/courses';

        this.$ajax.get(pathCourses)
            .then(response => {
                for (let i = 0; i < response.data.json_data.length; i++) {
                    let dataObj = response.data.json_data[i]
                    this.categories.courses.push(dataObj)
                }
                for (let i = 0; i < this.categories.courses.length; i++) {
                    let courseid = this.categories.courses[i].id
                    let currLabelPath = pathLabels + '/' + courseid
                    this.$ajax.get(currLabelPath)
                        .then(response => {
                            this.categories.labels[courseid] = response.data.json_list
                            console.log(this.categories.labels[courseid])
                        }).catch(error => {
                            console.log(error)
                        });
                }

            }).catch(error => {
                console.log(error);
            });
        for (let i = 0; i < this.categories.courses.length; i++) {
            //axios_csrf.get(pathLabels + '/' + this.courses[i].course_id)
            console.log("HELLO")
            console.log(this.categories.courses[i].course_id)
        }
        this.$ajax.get(pathLabels)
            .then(response => {
                console.log
                for (let i = 0; i < response.data.json_list.length; i++) {
                    let elem = response.data.json_list[i];
                    if (this.categories.labels[elem.course_id])
                        this.categories.labels[elem.course_id].push({
                            value: elem.name,
                            text: elem.name
                        });
                    else
                        this.categories.labels[elem.course_id] = [{
                            value: elem.name,
                            text: elem.name
                        }];
                }
            }).catch(error => {
                console.log(error);
            });
    },
}
</script>
