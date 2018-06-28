<template>
    <div v-if="$auth.ready()">
        <h2 class="form-header center-display">Login</h2>

    <form class="md-layout center-display" v-on:submit.prevent="checkUser">
        <md-card class="md-layout-item md-size-50 md-small-size-100">
            <md-card-content>

                <md-field>
                    <label for="email">Email address</label>
                    <md-input v-on:keyup="loginstatus = false" autofocus id="email" name="email" v-model="form.email" v-validate="'required'" type="email" />
                </md-field>
                <md-field>
                    <label for="studentnumber">Password</label>
                    <md-input v-on:keyup="loginstatus = false" autofocus id="psw" name="psw" v-model="form.psw" v-validate="'required'" type="password" />
                </md-field>
                <div v-show="errors.has('email')" class="invalid-feedback">
                    {{ errors.first('email') }}
                </div>
                <div v-show="errors.has('psw')" class="invalid-feedback">
                    {{ errors.first('psw') }}
                </div>
                <p id="loginfail" class="def-error-msg" v-show="this.loginstatus">
                    {{this.message}}
                </p>
                <md-button class="btn btn-primary" type="submit" v-bind:disabled="errors.any()">
                    Submit
                </md-button>
            </md-card-content>
        </md-card>
    </form>
</div>
</template>


<script>
import Vue from 'vue';
import VeeValidate from 'vee-validate';
import VueCookies from 'vue-cookies';
import Router from 'vue-router';

    Vue.use(VueCookies)

    export default {
        data() {
            return {
                form: {
                    email: '',
                    psw: ''
                },
                loginstatus: false,
                message: '',
                path: null
            }
        },
        methods: {
            // Log the student in.
            checkUser() {
                this.$validator.validateAll().then((result) => {
                    this.loginstatus = false
                    if (result) {
                        this.$auth.login({data: {
                            email: this.form.email,
                            password: this.form.psw
                            },
                            error: function (resp) {
                                // On failed login, show error
                                console.error(resp);
                                this.message = resp.response.data.json_data
                                this.loginstatus = true
                            }
                        });
                    }
                    }
                )
            }
        },
        /*
         * Redirect user if user is not logged in.
         */
        mounted() {
            window.$rederict_to_ticket = this.$route.query.redirect
            console.log(window.$rederict_to_ticket)
            if (this.$user.logged_in()) {
                if (window.$rederict_to_ticket){
                    this.$router.push('/ticket/'+window.$rederict_to_ticket)
                    window.$rederict_to_ticket = null
                }
                else{
                    this.$router.back()
                }
            }
        }
    }
</script>

<!-- Below necessary? -->
<style lang="scss" scoped></style>
