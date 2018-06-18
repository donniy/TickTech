<template>
    <section>
        <h1>Login</h1>

        <section>
            <!--Student name and number  -->
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
                        const path = '/auth'
                        this.$ajax.post(path, {
                            username: this.form.username,
                            password: "JWT is cool!!!"
                        }, response => {
                            // TODO: Implement authentication on back-end to work with Canvas.
                            window.$cookies.set('token', response.data.access_token)
                            this.form.username = ''
                            this.$ajax.get('/api/user/retrieve', response => {

                                let params = this.$route.params
                                let url = '/home'
                                if (typeof params !== 'undefined' && typeof params.prev_url !== 'undefined' && params.prev_url !== '/')
                                    url = params.prev_url
                                if (this.$user.set(response.data.json_data.user))
                                    this.$router.push(url)
                                else
                                    console.log("Can\'t set user.")
                            })
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