<!-- Login.vue shows the login page for a user, TODO: currently only asks for a student id (no password or anything). -->
<template>
    <section>
        <h1>Login</h1>
        <section>
            <form v-on:submit.prevent="checkUser">
                <div class="form-group">
                    <label for="studentnumber">Student ID</label>
                    <input class="form-control" id="studentid" name="studentid" v-model="form.username" v-validate="'required'" type="number"
                        placeholder="Student ID">
                    <div v-show="errors.has('studentid')" class="invalid-feedback">
                        {{ errors.first('studentid') }}
                    </div>
                </div>

                <button class="btn btn-primary">
                    Submit
                </button>
            </form>
        </section>
    </section>
</template>


<script>
    import Vue from 'vue'
    import VeeValidate from 'vee-validate'
    import VueCookies from 'vue-cookies'
    import Router from 'vue-router'

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
                        this.$auth.login({
                            url: '/auth',
                            data: { username: this.form.username, password: "TickTech" },
                            success: function (response) {
                                this.$auth.token(null, response.data.access_token)
                                this.$auth.fetch({
                                    params: {},
                                    success: function () {
                                        this.$router.push('/home')
                                    },
                                    error: function (response_fetch) {
                                        console.error(response_fetch)
                                    },
                                })
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

<!-- Below necessary? -->
<style lang="scss" scoped></style>