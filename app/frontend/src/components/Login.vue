<template>
<div>
	<h2 class="form-header center-display">Login</h2>

	<form class="md-layout center-display" v-on:submit.prevent="checkUser">
		<md-card class="md-layout-item md-size-50 md-small-size-100">
			<md-card-content>

				<md-field>
					<label for="email">Email address</label>
					<md-input autofocus id="email" name="email" v-model="form.email" v-validate="'required'" type="email" />
				</md-field>
				<md-field>
					<label for="studentnumber">Password</label>
					<md-input autofocus id="psw" name="psw" v-model="form.psw" v-validate="'required'" type="password" />
				</md-field>
				<div v-show="errors.has('email')" class="invalid-feedback">
					{{ errors.first('email') }}
				</div>
				<div v-show="errors.has('psw')" class="invalid-feedback">
					{{ errors.first('psw') }}
				</div>
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
                    username: '',
                }
            }
        },
        methods: {
            // Confirm the student ID.
            // TODO: Give error message if ID is wrong - maybe pop-up window?
            checkUser() {
                this.$validator.validateAll().then((result) => {
                    if (result) {
                        this.$auth.login({url: '/api/login',
                                        data: {username: this.form.username, password: "TickTech"},
                                          success: function (response) {
                                              this.$auth.token(null,
                                                               response.data.json_data.access_token);
                                              this.$auth.fetch({
                                                  data: {},
                                                  success: function () {
                                                      this.$router.push('/home');
                                                  },
                                                  error: function (response_fetch) {
                                                      console.error(response_fetch)
                                                  },
                                              });
                                        },
                                        error: function (response) {
                                            console.error(response)
                                        },
                                        rememberMe: true,
                                        fetchUser: false,
                                        //redirect: '/home',
                        })
                    }
                })
            },

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

<!-- Below necessary? -->
<style lang="scss" scoped></style>
