
<template>
<div>
    <div class="md-layout center-display">
    <form class="md-layout-item md-size-60 md-small-size-100" v-on:submit.prevent="Register">
        <md-steppers class="md-elevation-5" :md-active-step.sync="active" md-sync-route md-dynamic-height>
            <md-step :md-error="firstStepError" id="first" md-label="Student details" :md-done.sync="first" md-description="Required">
                <md-field>
                    <label for="email">Email address</label>
                    <md-input autofocus v-on:keyup="checkEmailAvailability" id="email" name="email" v-model="form.email" v-validate="'required'" type="email" />
                </md-field>
                <p class="def-error-msg" v-show="this.emailstatus">
                    This email address is taken.
                </p>
                <md-field>
                    <label for="studentid">Student ID</label>
                    <md-input v-on:keyup="checkIDAvailability" id="studentid" name="studentid" v-model="form.studentid" v-validate="'required'" type="tel" />
                </md-field>
                <p class="def-error-msg" v-show="this.idstatus">
                    This student id is taken.
                </p>
                <md-field>
                    <label for="name">Full Name</label>
                    <md-input autofocus id="name" name="name" v-model="form.name" v-validate="'required'" type="text" />
                </md-field>
                <div class="center-display">
                    <md-button class=" btn btn-primary" @click="nextArea" v-bind:disabled="checkErrors">
                        Next
                    </md-button>
                </div>
            </md-step>
            <md-step @click="setError(1)" :md-active="second" :md-done.sync="second" id="second" md-label="Password" md-description="Required">
                <md-field>
                    <label for="password">Password</label>
                    <md-input tabindex="-1" id="password" name="password" v-model="form.password" v-validate="'required'" type="password" />
                </md-field>
                <md-field>
                    <label for="password_confirmation">Repeat password</label>
                    <md-input tabindex="-1" v-on:keyup="checkPswConfirmation" id="password_confirmation" name="password_confirmation" v-model="form.password_confirmation" v-validate="'required'" type="password" />
                </md-field>
                <div class="alert alert-danger" v-show="checkErrors">
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
                    <div v-if="this.idstatus">
                        Check your student id!
                    </div>
                    <div v-if="this.emailstatus">
                        Check your email address!
                    </div>

                    <div v-if="!this.pswstatus">
                        Passwords do not match!
                    </div>
                </div>
                <div class="center-display">
                    <md-button tabindex="-1" type="submit" class=" btn btn-primary" v-bind:disabled="checkErrors">
                        Register
                    </md-button>
                </div>

                <p class="def-error-msg" v-show="checkErrors">
                    Please fill out the form correctly.
                </p>
            </md-step>
        </md-steppers>
    </form>
</div>
</div>
</template>


<script>
import VeeValidate from 'vee-validate'
import Router from 'vue-router'

export default {
    data() {
        return {
            form: {
                name: "",
                studentid: "",
                email: "",
                password: "",
                password_confirmation: "",

            },
            emailstatus: false,
            idstatus: false,
            pswstatus: true,
            first: false,
            second: false,
            secondStepError: null,
            firstStepError: null,
            active: 'first'
        }
    },
    methods: {
        Register() {
            this.$validator.validateAll().then((result) => {
                if (result) {
                    const path = '/api/user/register';
                    this.$ajax.post(path, this.form, response => {
                        console.log(response);
                        if (response.data.json_data["status"] != "OK") {
                            window.alert("We could not register you at this time!\n" + response.data.json_data["status"] )
                            return
                        } else {
                            this.$auth.login({data: {
                                email: this.form.email,
                                password: this.form.password
                                },
                                error: function (resp) {
                                    window.alert("Authentication is down!")
                                    console.error(resp);
                                }
                            });
                        }
                    })
                }
            })
        },
        checkEmailAvailability() {
            const path = '/api/user/exists'
            this.$ajax.post(path, {
                email: this.form.email
            }, response => {
                this.emailstatus = response.data.json_data.status;
                console.log(this.emailstatus)

            })
        },
        checkIDAvailability() {
            const path = '/api/user/idexists';
            this.$ajax.post(path, {
                studentid: this.form.studentid
            }, response => {
                this.idstatus = response.data.json_data.status;
                console.log(this.idstatus)

            })
        },
        checkPswConfirmation() {
            this.pswstatus = (this.form.password === this.form.password_confirmation) || this.form.password === ""
        },
        nextArea() {

            if (this.setError(1)) {
                this.firstStepError = null
                this.active = 'second'
            } else {

            }
        },
        setError(step) {
            if (step == 1) {
                if (this.emailstatus || this.idstatus || this.form.email.length == 0 || this.form.studentid.length == 0 || this.form.name.length == 0) {
                    this.firstStepError = 'Please fill out the form'
                    this.first = false
                    return false
                } else {
                    this.first = true
                    return true
                }
            } else if (step == 2) {
                if (this.form.password.length == 0 || this.form.password_confirmation.length == 0 || !this.pswstatus) {
                    this.secondStepError = 'Error found'
                    this.second = false
                } else {
                    this.second = true
                }
            }
        }
    },
    computed: {
        checkErrors() {
            return this.errors.any() || this.idstatus || this.emailstaus || !this.pswstatus
        }
    }
}
</script>
