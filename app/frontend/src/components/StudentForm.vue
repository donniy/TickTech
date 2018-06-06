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
                            <label for="category">Category</label>
                            <select id="category" class="form-control custom-select" v-model="form.label_class">
                                <option disabled value="">Nothing selected</option>
                                <option v-for="option in options.labels" v-bind:value="option.value">
                                {{ option.text }}
                                </option>
                            </select>

                        </div>

                        <button class="btn btn-primary">
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
                labels: [
                    { value: "Assignment 1", text: "Ass1" },
                    { value: "Assignment 2", text: "Ass2" },
                    { value: "Assignment 3", text: "Ass3" },
                    { value: "Deadlines", text: "Deadlines" },
                    { value: "Absense", text: "Absense" },
                    { value: "Course guide", text: "Course" }
                ]
            }
        }
    },
    mounted: function() {
        this.$emit('tab-activate', 'submit-ticket')
    }
}

</script>
