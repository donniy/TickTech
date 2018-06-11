<template>
    <div>
        <div>
            <section>
                <h1>Register account</h1>

                <section>
                    <form v-on:submit.prevent="Register">
                        <div class="form-group">
                            <label for="name">Full name</label>
                            <input id="name" class="form-control" name="name" v-model="form.name" v-validate="'required|min:1'" type="text" placeholder="Full name">
                        </div>

                        <div class="form-group">
                            <label for="studentid">Student ID</label>
                            <input class="form-control" id="studentid" name="studentid" v-model="form.studentid" v-validate="'required|min:1|numeric'" type="text" placeholder="Student ID">
                        </div>

                        <div class="form-group">
                            <label for="email">Email address</label>
                            <input id="email" class="form-control" name="email" v-model="form.email" v-validate="'required|min:1'" type="text" placeholder="Email address">
                        </div>

                        <div class="form-group">
                            <label for="password">Enter a password</label>
                            <input
                                id="password"
                                class="form-control"
                                v-validate="'required'"
                                name="password"
                                v-model="form.password"
                                type="password"
                                placeholder="Password">
                            </br>

                            <!-- <input
                                id="password_confirmation"
                                class="form-control"
                                v-validate="'required|confirmed:password'"
                                name="password_confirmation"
                                v-model="form.password_confirmation"
                                type="password"
                                placeholder="Password again!"> -->
                        </div>

                        <div class="alert alert-danger" v-show="errors.any()">
                            <div v-if="errors.has('name')">
                                {{ errors.first('name') }}
                            </div>
                            <div v-if="errors.has('studentid')">
                                {{ errors.first('studentid') }}
                            </div>
                            <div v-if="errors.has('email')">
                                {{ errors.first('email') }}
                            </div>
                            <div v-if="errors.has('password')">
                                {{ errors.first('password') }}
                            </div>
                            <!-- <div v-if="errors.has('password_confirmation')">
                                {{ errors.first('password_confirmation') }}
                            </div> -->
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
                // password_confirmation: "",
            }
        }
    }, methods: {
        Register () {
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
