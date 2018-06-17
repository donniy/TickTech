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
                            <input v-on:keyup="checkIDAvailability" class="form-control" id="studentid" name="studentid" v-model="form.studentid" v-validate="'required|min:1|numeric'"
                                type="text" placeholder="Student ID">
                        </div>
                        <p class="def-error-msg" v-show="this.idstatus">
                            This student id is taken.
                        </p>

                        <div class="form-group">
                            <label for="email">Email address</label>
                            <input v-on:keyup="checkEmailAvailability" id="email" class="form-control" name="email" v-model="form.email" v-validate="'required|min:1'"
                                type="text" placeholder="Email address">
                        </div>
                        <p class="def-error-msg" v-show="this.emailstatus">
                            This email address is taken.
                        </p>

                        <div class="form-group">
                            <label for="password">Enter a password</label>
                            <input id="password" class="form-control" v-validate="'required'" name="password" v-model="form.password" type="password"
                                placeholder="Password">
                            <br />

                            <input id="password_confirmation" class="form-control" v-validate="'required'" v-on:keyup="checkPswConfirmation" name="password_confirmation"
                                v-model="form.password_confirmation" type="password" placeholder="Repeat password">
                        </div>

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

                        <button type="submit" class="btn btn-primary" v-bind:disabled="checkErrors">
                            Register
                        </button>

                        <p class="def-error-msg" v-show="checkErrors">
                            Please fill out the form correctly.
                        </p>

                    </form>
                </section>
            </section>
        </div>
    </div>
</template>

<script>

    import VeeValidate from 'vee-validate';
    import Router from 'vue-router';

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

            }
        }, methods: {
            Register() {
                this.$validator.validateAll().then((result) => {
                    if (result) {
                        const path = '/api/user/register';
                        this.$ajax.post(path, this.form, response => {
                            console.log(response);
                            if (response.data.json_data["status"] == false) {
                                window.alert("Student id or email already taken!")
                                return
                            } else {
                                logUserIn()
                            }
                        });
                    }
                });
            }, checkEmailAvailability() {
                const path = '/api/user/exists';
                this.$ajax.post(path, { email: this.form.email }, response => {
                    this.emailstatus = response.data.json_data.status;
                    console.log(this.emailstatus)

                });
            }, checkIDAvailability() {
                const path = '/api/user/idexists';
                this.$ajax.post(path, { studentid: this.form.studentid }, response => {
                    this.idstatus = response.data.json_data.status;
                    console.log(this.idstatus)

                });
            }, checkPswConfirmation() {
                this.pswstatus = (this.form.password === this.form.password_confirmation) || this.form.password === ""
            }, logUserIn() {
                const path = '/auth';
                this.$ajax.post(path, {
                    username: this.form.studentid,
                    password: "JWT is cool!!!"
                }, response => {
                    // TODO: Implement authentication on backend work with Canvas.
                    window.$cookies.set('token', response.data.access_token);
                    console.log(response);
                    this.$ajax.get('/api/user/retrieve', response => {
                        if (this.$user.set(response.data.user))
                            this.$router.replace('/');
                        else
                            console.log("Can\'t set user.");
                    });
                });
            }
        }, computed: {
            checkErrors() {
                return this.errors.any() || this.idstatus || this.emailstaus || !this.pswstatus
            }
        }
    }


</script>