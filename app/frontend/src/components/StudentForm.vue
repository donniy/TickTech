<template>
    <div>
        <div>
            <section>
                <h1>Submit a question to the mailing list</h1>

                <section>
                    <!--Student name and number  -->
                    <form v-on:submit.prevent="sendTicket">
                        <div class="form-group">
                            <label for="name">Full name</label>
                            <input id="name" class="form-control" name="name" v-model="form.name" v-validate="'required|min:1'" type="text" placeholder="Full name">
                            <div v-show="errors.has('name')" class="invalid-feedback">
                                {{ errors.first('name') }}
                            </div>
                        </div>

                        <div class="form-group">
                            <label for="studentid">Student ID</label>
                            <input class="form-control" id="studentid" name="studentid" v-model="form.studentid" v-validate="'required|min:1|numeric'" type="text" placeholder="Student ID">
                            <div v-show="errors.has('studentid')" class="invalid-feedback">
                                {{ errors.first('studentid') }}
                            </div>
                        </div>

                        <div class="form-group">
                            <label for="email">Email address</label>
                            <input id="email" class="form-control" name="email" v-model="form.email" v-validate="'required|min:1'" type="text" placeholder="Email address">
                            <div v-show="errors.has('email')" class="invalid-feedback">
                                {{ errors.first('email') }}
                            </div>  
                        </div>

                        <div class="form-group">
                            <input id="subject" class="form-control-title" v-validate="'required|max:50'"name="subject" v-model="form.subject" type="text" placeholder="Subject">
                            <div v-show="errors.has('subject')" class="invalid-feedback">
                                {{ errors.first('subject') }}
                            </div>
                        </div>

                        <div class="form-group">
                            <textarea-autosize id="message" class="form-control" name="message" v-validate="'required'" placeholder="Message" v-model="form.message"></textarea-autosize>
                            <div v-if="errors.has('message')" class="invalid-feedback">
                                {{ errors.first('message') }}
                            </div>
                        </div>

                        <div class="form-group">
                            <label for="course">Course</label>
                            <select id="course" v-validate="'required'" class="form-control custom-select" v-model="form.courseid">
                                <option disabled value="">Nothing selected</option>
                                <option v-for="option in categories.courses" v-bind:value="option.id">
                                {{ option.name }}
                                </option>
                            </select>

                        </div>
                        <div class="form-group">
                            <label for="category">Category</label>
                            <select id="category" v-validate="'required'" class="form-control custom-select" v-model="form.labelid">
                                <option disabled value="">Nothing selected</option>
                                <option v-for="option in categories.labels[form.courseid]" v-bind:value="option.value">{{ option.text }}</option>
                            </select>

                        </div>

                        <button type="submit" class="btn btn-primary" v-bind:disabled="errors.any()">
                            Submit
                        </button>

                        <p class="def-error-msg" v-show="errors.any()">
                        Please fill out the form correctly
                        </p>

                    </form>
                </section>
            </section>
        </div>
    </div>
</template>

<script>

import axios from 'axios'
import VeeValidate from 'vee-validate';

const axios_csrf = axios.create({
    headers: {'X-CSRFToken': csrf_token}
});

export default {
    data () {
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
                courses:[],
                labels: {}
            }
        }
    }, computed: {
        options: function(event) {
            return categories.labels[form.courseid]
        }
    }, methods: {
        sendTicket () {
            this.$validator.validateAll()
            const path = '/api/ticket/submit'
            axios_csrf.post(path, this.form)
            .then(response => {
                this.$router.push({name: 'StudentViewTicket', params: {ticket_id: response.data.ticketid}})
                this.form = ''
            }).catch(error => {
                console.log(error)
            })
        },
        onChange: function(e) {
            console.log(event.srcElement.value);
            this.categories = this.categories
        },
        mounted: function() {

        }
    },
    mounted () {
        const pathLabels = '/api/labels';
        const pathCourses = '/api/courses';

        axios_csrf.get(pathCourses)
        .then(response => {
            this.categories.courses = response.data;
        }).catch(error => {
            console.log(error);
        });

        axios_csrf.get(pathLabels)
        .then(response => {
            for(let i = 0; i < response.data.json_list.length; i++) {
                let elem = response.data.json_list[i];
                if (this.categories.labels[elem.course_id])
                    this.categories.labels[elem.course_id].push({value: elem.name, text: elem.name});
                else
                    this.categories.labels[elem.course_id] = [{value: elem.name, text: elem.name}];
            }
        }).catch(error => {
            console.log(error);
        });
    },
}


</script>
