<template>
    <div>
        <div>
            <section>
                <h1>Register account</h1>

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
                            <label for="password">Enter a password</label>
                            <input id="password" class="form-control" v-validate="'required|max:50'"name="password" v-model="form.subject" type="password" placeholder="password">
                            <div v-show="errors.has('password')" class="invalid-feedback">
                                {{ errors.first('password') }}
                            </div>
                        </div>

                        <div class="form-group">
                            <input id="repassword" class="form-control" v-validate="'required|max:50'"name="repassword" v-model="form.subject" type="repassword" placeholder="repeat password">
                            <div v-show="errors.has('repassword')" class="invalid-feedback">
                                {{ errors.first('repassword') }}
                            </div>
                        </div>

                        <button type="submit" class="btn btn-primary" v-bind:disabled="errors.any()">
                            Register
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
                password: "",
                repassword: "",
            }
        }
    }, methods: {
        sendTicket () {
            this.$validator.validateAll()
            const path = '/api/user/register'
            axios_csrf.post(path, this.form)
                .then(response => {

                    console.log("Registered")
                    this.form = ""
                }).catch(error => {
                    console.log(error)
                })
        }
    }
}


</script>
