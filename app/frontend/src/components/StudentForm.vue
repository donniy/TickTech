<template>
    <div>
        <div>
            <section>
                <h1>Submit a question to the Mailing list</h1>

                <section>
                    <!--Student name and number  -->
                    <form v-on:submit.prevent="sendTicket;">
                        <div class="form-group">
                            <label for="name">Name</label>
                            <input id="name" class="form-control" name="name" v-model="form.name" v-validate="'required|min:1'" type="text" placeholder="Full name">
                            <div v-show="errors.has('name')" class="invalid-feedback">
                                {{ errors.first('name') }}
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="studentnumber">Student number</label>
                            <input class="form-control" id="studentnumber" name="studentnumber" v-model="form.sudentid" v-validate="'required|min:5'" type="number" placeholder="Student Number">
                            <div v-show="errors.has('StudentID')" class="invalid-feedback">
                                {{ errors.first('StudentID') }}
                            </div>
                        </div>

                        <div class="form-group">
                            <label for="message">Message</label>
                            <textarea id="message" class="form-control" name="message" v-validate="'required'" placeholder="Message" v-model="form.message"></textarea>
                            <div v-if="errors.has('message')" class="invalid-feedback">
                                {{ errors.first('message') }}
                            </div>
                        </div>

                        <div class="form-group">
                            <label for="course">Course</label>
                            <select id="course" class="form-control custom-select" v-model="form.courseid">
                                <option disabled value="">Nothing selected</option>
                                <option v-for="option in categories.courses" v-bind:value="option.value">
                                {{ option.text }}
                                </option>
                            </select>

                        </div>
                        <div class="form-group">
                            <label for="category">Category</label>
                            <select id="category" class="form-control custom-select" v-model="form.label_class">
                                <option disabled value="">Nothing selected</option>
                                <option v-for="option in categories.labels[form.courseid]" v-bind:value="option.value">{{ option.text }}</option>
                            </select>

                        </div>

                        <button v-on:click="sendTicket" class="btn btn-primary" v-bind:disabled="errors.any()">
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
                StudentID: "",
                message: "",
                courseid: "",
                label_class: "",
            },  categories: {
                courses:[
                    { value: "Prosoft", text: "Project software engineering"},
                    { value: "ATF", text: "Automaten en formele talen"},
                    { value: "OS", text: "Operating systems"}
                ], labels: {
                    Prosoft: [
                        { value: "Ass1", text: "Assignment 1" },
                        { value: "Ass2", text: "Assignment 2" },
                        { value: "Ass3", text: "Assignment 3" },
                        { value: "Deadlines", text: "Deadlines" },
                        { value: "Absense", text: "Absense" },
                        { value: "Course", text: "Course Guide" }
                    ], ATF: [
                        { value: "Ass1", text: "Klachten" },
                        { value: "Ass2", text: "Meer klachten" },
                        { value: "Ass3", text: "Klachten extra" },
                        { value: "Deadlines", text: "Deadlines" },
                        { value: "Absense", text: "Absense" },
                        { value: "Course", text: "Course Guide" }
                    ], OS: [
                        { value: "Ass1", text: "Hackme1" },
                        { value: "Ass2", text: "Schedulers" },
                        { value: "Ass3", text: "Cijfer info" },
                        { value: "Deadlines", text: "Deadlines" },
                        { value: "Absense", text: "Absense" },
                        { value: "Course", text: "Course Guide" }
                    ]
                }
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
                this.form = ''
                window.location = "/";
            }).catch(error => {
                    console.log(error)
            })

        }, onChange: function(e) {
          console.log(event.srcElement.value);
          this.categories = this.categories
        },
        mounted: function() {
            this.$emit('tab-activate', 'submit-ticket')
        }
    }
}

</script>
