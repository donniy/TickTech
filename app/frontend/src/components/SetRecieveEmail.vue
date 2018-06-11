<template>
    <div>
        <div>
            <section>
                <h1>Create a new email fetcher</h1>

                <section>
                    <!--Student name and number  -->
                    <form v-on:submit.prevent="sendTicket">
                        <div class="form-group">
                            <label for="name">email adress</label>
                            <input id="name" class="form-control" name="name" v-model="form.name" v-validate="'required|min:1'" type="text" placeholder="uvapsetest@gmail.com">
                            <div v-show="errors.has('name')" class="invalid-feedback">
                                {{ errors.first('name') }}
                            </div>
                        </div>

                        <div class="form-group">
                            <label for="studentid">pop3 settings</label>
                            <input class="form-control" id="studentid" name="studentid" v-model="form.studentid" v-validate="'required|min:1|numeric'" type="text" placeholder="pop.gmail.com">
                            <div v-show="errors.has('studentid')" class="invalid-feedback">
                                {{ errors.first('studentid') }}
                            </div>
                        </div>

                        <div class="form-group">
                            <label for="email">Port</label>
                            <input id="email" class="form-control" name="email" v-model="form.email" v-validate="'required|min:1'" type="text" placeholder="995">
                            <div v-show="errors.has('email')" class="invalid-feedback">
                                {{ errors.first('email') }}
                            </div>
                        </div>

                        <div class="form-group">
                            <label for="category">Password</label>
                            <input id="email" class="form-control" name="email" v-model="form.email" v-validate="'required|min:1'" type="text" placeholder="stephanandrea">

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
