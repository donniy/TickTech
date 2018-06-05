<template>
    <div>
        <div>
            <section>
                <h1>Submit a question to the Mailing list</h1>

                <section>
                    <!--Student name and number  -->
                    <form v-on:submit.prevent="$validator.validateAll(); console.log(form);">
                        <div>
                            <label>Name and student number</label>
                            <div>
                                <input name="name" v-model="form.name" v-validate="'required|min:1'" type="text" placeholder="Full name">
                            </div>
                            <div>
                                <input name="name" v-model="form.sudentid" v-validate="'required|min:5'" type="number" placeholder="Student Number">
                            </div>
                        </div>

                        <div>
                            <label>Message</label>
                            <div>
                                <textarea name="message" v-validate="'required'" placeholder="Message" v-model="form.message"></textarea>
                            </div>
                        </div>

                        <div>
                            <label>Category</label>
                            <div>
                                <div>
                                    <select v-model="form.label_class">
                                        <option disabled value="">Nothing selected</option>
                                        <option v-for="option in options.labels" v-bind:value="option.value">
                                            {{ option.text }}
                                        </option>
            					    </select>
                                </div>
                            </div>
                        </div>

                        <div>
                            <div>
                                <button>
            								Submit
            			        </button>
                            </div>
                        </div>

                    </form>
                </section>
            </section>
        </div>
    </div>
</template>

<script>


import axios from 'axios'

export default {
    data () {
        return {
            form: {
                name: "",
                studentid: "",
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
    }
}

</script>
