<template>
    <div>
        <h2 class="form-header center-display">Demo login</h2>

        <form class="md-layout center-display" v-on:submit.prevent="checkUser">
            <md-card class="md-layout-item md-size-50 md-small-size-100">
                <md-card-content>

                    <md-field>
                    <label for="studentnumber">Student ID</label>
                    <md-input class="form-control" id="studentnumber" name="studentnumber" v-model="form.username" v-validate="'required'" type="number"/>
                    <div v-show="errors.has('studentid')" class="invalid-feedback">
                        {{ errors.first('studentid') }}
                    </div>
                    <md-button type="submit" v-bind:disabled="errors.any()">
                        Submit
                    </md-button>
                </md-field>
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
                    username: '',
                }
            }
        },
        methods: {
            checkUser() {
                this.$validator.validateAll().then((result) => {
                    if (result) {
                        this.$auth.login({url: '/api/login',
                                        data: {username: this.form.username, password: "TickTech"},
                                          success: function (response) {
                                              this.$auth.token(null,
                                                               response.data.json_data.access_token);
                                              console.log("TOKEN:")
                                              console.log(response.data.json_data);
                                              console.log(this.$auth.token())
                                              this.$auth.fetch({
                                                  data: {'acces_token': this.$auth.token()},
                                                  success: function () {
                                                      console.log("USER:")
                                                      console.log(this.$auth.user())
                                                      this.$router.push('/home');
                                                  },
                                                  error: function (response_fetch) {
                                                      console.log("ERROR")
                                                      console.error(response_fetch)
                                                  },
                                              });
                                        },
                                        error: function (response) {
                                            console.error(response)
                                        },
                                        rememberMe: true,
                                        fetchUser: false,
                                        // redirect: '/home',
                        })
                    }
                })
            }
        },
        mounted() {
            if (this.$user.logged_in()) {
                this.$router.back()
            } else {
                window.$cookies.remove('token')
                window.$cookies.remove('user')
            }
        }
    }
</script>

<style lang="scss" scoped>
</style>
