<template>
    <section>
        <h1>Login</h1>

        <section>
            <!--Student name and number  -->
            <form v-on:submit.prevent="checkUser">
                <div class="form-group">
                    <label for="studentnumber">Student number</label>
                    <input class="form-control" id="studentnumber" name="studentnumber" v-model="form.studentid" pattern="\d{4}\d+" v-validate="'required'" type="text" placeholder="Student Number">
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
import axios from 'axios';
import VueCookies from 'vue-cookies';
import Router from 'vue-router';

Vue.use(VueCookies);

const axios_csrf = axios.create({
    headers: {
        'X-CSRFToken': csrf_token,
    }
});

export default {
    data () {
        return {
            form : {
                studentid: '',
            }
        }
    },
    methods: {
        checkUser() {
            this.$validator.validateAll().then((result) => {
                if(result) {
                    const path = '/api/login/';
        
                    const msg = JSON.stringify(this.form);
                    console.log(msg);
                    axios_csrf.get(path)
                    .then(response => {
                        console.log(response);
                        // TODO: Implement authentication on back-end to work with Canvas.
                        this.$cookies.set('usr', this.form.studentid);
                        this.form.studentid = '';
                        this.$router.replace('/');
                    })
                    .catch(error => {
                        console.log(error);
                    });
                }
            });
        }
    }
}
</script>


<style lang="scss" scoped>

</style>
