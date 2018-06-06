<template>
    <div>
        <div>
            <section>
                <h1>Submit a question to the Mailing list</h1>

                <section>
                    <!--Student name and number  -->
                    <form v-on:submit.prevent="$validator.validateAll(); console.log(form);">
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
                            <select id="course" class="form-control custom-select" v-model="form.label_class">
                                <option disabled value="">Nothing selected</option>
                                <option v-for="option in options.courses" v-bind:value="option.value">
                                {{ option.text }}
                                </option>
                            </select>

                        </div>
                        <div class="form-group">
                            <label for="category">Category</label>
                            <select id="category" class="form-control custom-select" v-model="form.label_class">
                                <option disabled value="">Nothing selected</option>
                                <option v-for="option in options" v-bind:value="option.value">{{ option.text }}</option>
                            </select>

                        </div>

                        <button class="btn btn-primary" v-bind:disabled="errors.any()">
                            Submit
                        </button>

                    </form>
                </section>
            </section>
        </div>
    </div>
</template>

<script>

import axios from 'axios'
import VeeValidate from 'vee-validate';

export default {
    data () {
        return {
            form: {
                name: "",
                StudentID: "",
                message: "",
                label_class: "",
            },
            options: {
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
            return labels[this.category]
        }
    }, methods: {
        sendForm () {
        const path = '/api/ticket/' + this.$route.params.ticket_id + '/submit'
        axios_csrf.post(path, {message: this.form})
        .then(response => {
            this.messages.push(response.data.message)
            this.reply = ''
            })
            .catch(error => {
                console.log(error)
            })
        }
    }, onChange: function(e) {
      console.log(event.srcElement.value);
      this.options = this.options
    }
}

</script>
