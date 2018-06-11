<template>
    <div>
        <div>
            <section>
                <h1>Setup a fetcher to your mailinglist.</h1>

                <section>
                    <!--Student name and number  -->
                    <form @submit.prevent="handleSubmit">
                        <div class="form-group">
                            <label for="email">Email address</label>
                            <input id="email" class="form-control" name="email" v-model="form.email" v-validate="'required|min:1'" type="text" placeholder="uvapsetest@gmail.com">
                            <div v-show="errors.has('email')" class="invalid-feedback">
                                {{ errors.first('email') }}
                            </div>
                        </div>

                        <div class="form-group">
                            <label for="category">Password</label>
                            <input id="password" class="form-control" name="password" v-model="form.password" v-validate="'required|min:1'" type="text" placeholder="stephanandrea">
                        </div>

                        <div class="form-group">
                            <label for="pop">Pop3 settings</label>
                            <input class="form-control" id="pop" name="pop" v-model="form.pop" v-validate="'required|min:1'" type="text" placeholder="pop.gmail.com">
                            <div v-show="errors.has('pop')" class="invalid-feedback">
                                {{ errors.first('pop') }}
                            </div>
                        </div>

                        <div class="form-group">
                            <label for="port">Port</label>
                            <input id="port" class="form-control" name="port" v-model="form.port" v-validate="'required|min:1'" type="text" placeholder="995">
                            <div v-show="errors.has('port')" class="invalid-feedback">
                                {{ errors.first('port') }}
                            </div>
                        </div>

                        <button type="submit" class="btn btn-primary" v-bind:disabled="errors.any()">
                            Submit
                        </button>

                        <p class="def-error-msg" v-show="errors.any()">
                            Please fill out the form correctly.
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
        this.$validator.validateAll()
        return {
            form: {
                email: "uvapsetest@gmail.com",
                password: "stephanandrea",
                pop: "pop.gmail.com",
                port: "995"
            }
        }
    },
    methods: {
        getCourseEmailSettings () {
          this.status = 'getting info'
          const path = '/api/fetch/' + this.$route.params.course_id + '/tickets'
          axios.get(path)
          .then(response => {
            this.tickets = response.data.json_data
            this.status = 'Retrieved data'
            console.log(response.data.json_data)
            console.log(response)
          })
          .catch(error => {
            console.log(error)
            this.status = 'failed getting tickets'
          })
        },
        handleSubmit () {
            this.$validator.validateAll()
            const path = '/api/fetch/submit'
            axios_csrf.post(path, this.form)
            .then(response => {
            //     this.$router.push({name: 'StudentViewTicket', params: {ticket_id: response.data.ticketid}})
                this.form = ''
                console.log(data)
            }).catch(error => {
                console.log(error)
            })
        }
    }
}

</script>
