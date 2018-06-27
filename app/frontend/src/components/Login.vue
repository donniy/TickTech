<template>
    <div v-if="$auth.ready()">
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
            // Confirm the student ID.
            // TODO: Give error message if ID is wrong - maybe pop-up window?
            checkUser() {
                this.$validator.validateAll().then((result) => {
                    if (result) {
                        this.$auth.login({data: {
                            username: this.form.username,
                            password: "TickTech"
                            },
                            error: function (resp) {
                                console.error(resp);
                            }
                        });
                    }
                    }
                )
            }
        },
        mounted() {
            if (this.$user.logged_in()) {
                this.$router.back()
            }
        }
    }
</script>

<!-- Below necessary? -->
<style lang="scss" scoped></style>
