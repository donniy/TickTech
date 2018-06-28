<template>
    <transition name="modal">
        <div class="modal-mask">
            <div class="modal-wrapper">
                <div class="modal-container">
                    <div class="modal-body">
                        <slot name="body">
                            <h1>{{warning}}</h1>
                            <!--Student name and number  -->
                            <form @submit.prevent="handleSubmit">
                                <div class="form-group">
                                    <input type="hidden" name="course_id" v-model="form.course_id" />

                                    <label for="email">Email address</label>
                                    <input id="email" class="form-control" name="email" v-model="form.email" v-validate="'required|min:1'" type="email" placeholder="uvapsetest@gmail.com">

                                    <label for="category">Password</label>
                                    <input id="password" class="form-control" name="password" v-model="form.password" v-validate="'required|min:1'" type="password">

                                    <label for="pop">Pop3 settings</label>
                                    <input class="form-control" id="pop" name="pop" v-model="form.pop" v-validate="'required|min:1'" type="text" placeholder="pop.gmail.com">

                                    <label for="port">Port</label>
                                    <input id="port" class="form-control" name="port" v-model="form.port" v-validate="'required|min:1'" type="text" placeholder="995">

                                    <p for="error" class="def-error-msg subheading-middle" v-show="error.show">{{error.text}}</p>
                                </div>
                            </form>
                            <div class="row">
                                <div class="col-sm-4">
                                    <button type="submit" class="btn btn-primary" v-on:click="newEmailSettings">
                                        {{ button.text }}
                                    </button>
                                </div>
                                <div class="col-sm-4 subheading-middle">
                                    <button v-show="isRunning" class="btn btn-primary middle-button" v-on:click="stopThread">
                                        Stop
                                    </button>
                                </div>
                                <div class="col-sm-4">
                                    <button class="btn btn-primary close-button" @click="$emit('close')">
                                        Cancel
                                    </button>
                                </div>
                            </div>
                            <div class="subheading-middle" v-show="isLoading">
                                <Circle8></Circle8>
                            </div>
                        </slot>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script>
    import { Circle8 } from 'vue-loading-spinner'

    export default {
        props: ['warning'],
        data: function () {
            return {
                form: {
                    email: "uvapsetest@gmail.com",
                    password: "stephanandrea",
                    pop: "pop.gmail.com",
                    port: "995",
                    course_id: this.$route.params.course_id
                },
                button: {
                    text: "Start"
                },
                isRunning: false,
                isLoading: false,
                error: {
                    show: false,
                    text: ""
                }
            };
        },
        methods: {

            /*
             * Check if all fields are not empty and if they are valid.
             */
            checkForm: function () {
                this.error.text = ''
                if (this.form.password == "") this.error.text = ("Password required.");
                if (this.form.pop == "") this.error.text = ("Server required.");
                if (this.form.port == "") this.error.text = ("Port required.");
                if (this.form.email == "") {
                    this.error.text = ("Email required.");
                }
                else {
                    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                    if (!re.test(this.form.email)) {
                        this.error.text = "Valid email required"
                    }

                }
                if (this.error.text != '') {
                    this.error.show = true
                    return false
                }
                return true
            },

            /*
             * Setup new email server with new email settings.
             */
            newEmailSettings() {
                this.error.show = false
                this.error.text = ''
                const path = '/api/email'
                if (this.checkForm()) {
                    console.log("i will  emit")
                    this.isLoading = true
                    this.$socket.emit('setup-email', {
                        email: this.form.email,
                        password: this.form.password,
                        pop: this.form.pop,
                        port: this.form.port,
                        course_id: this.form.course_id
                    })
                }
                console.log("emitted")
            },

            /*
             * Stop email server. 
             */ 
            stopThread() {
                const path = '/api/email/stop'
                this.$ajax.post(path, this.form, response => {
                    if (response.status == 201) {
                        this.$parent.showEmailModal = false
                    }
                    if (response.status == 200) {
                        this.error.show = true
                        this.error.text = response.data.json_data
                    }
                })
            }
        },
        beforeCreate: function () {
            // Get the current email settings from server
            const path = '/api/email/' + this.$route.params.course_id + '/settings'
            this.$ajax.get(path, response => {
                // TODO: Implement authentication on back-end to work with Canvas.
                if (response.status == 201) {
                    if (response.data.json_data.email != null) {
                        this.form.email = response.data.json_data.email
                    }
                    if (response.data.json_data.password != null) {
                        this.form.password = response.data.json_data.password
                    }
                    if (response.data.json_data.pop != null) {
                        this.form.pop = response.data.json_data.pop
                    }
                    if (response.data.json_data.port != null) {
                        this.form.port = response.data.json_data.port
                    }

                    if (response.data.json_data.running) {
                        this.button.text = "Update"
                        this.isRunning = true

                    }
                }

                if (response.status == 200) {
                    this.error.show = true
                    this.error.text = response.data.json_data
                }
            })
        },
        sockets: {
            'setup-email': function (data) {
                if (data.result != "update") {
                    this.isLoading = false
                }
                else {
                    console.log(data.data)
                }
                console.log("recieve data")
                console.log(data)
                console.log(data.result)
                if (data.result == 'succes') {
                    console.log("SUCCES")
                    this.$parent.showEmailModal = false
                }
                if (data.result == 'fail') {
                    console.log('fail')
                    this.error.show = true
                    this.error.text = data.data
                }
                console.log("finished")
            }
        },
        components: {
            Circle8
        }
    }
</script>
<style>
    .modal-mask {
        position: fixed;
        z-index: 9998;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, .5);
        display: inline-table;
        transition: opacity .3s ease;
    }

    .modal-wrapper {
        display: table-cell;
        vertical-align: middle;
    }

    .modal-container {
        width: 50%;
        margin: auto auto;
        padding: auto auto;
        background-color: #fff;
        border-radius: 2px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
        transition: all .3s ease;
        font-family: Helvetica, Arial, sans-serif;
    }

    .modal-header h3 {
        margin-top: 0;
        color: #42b983;
    }

    .modal-body {
        /* margin: 20px 0; */
        overflow-y: auto;
        padding: 50px 50px;
    }

    .modal-default-button {
        float: right;
    }

    .modal-stop-button {
        float: left;
    }

    /*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

    .modal-enter {
        opacity: 0;
    }

    .modal-leave-active {
        opacity: 0;
    }

    .modal-enter .modal-container,
    .modal-leave-active .modal-container {
        -webkit-transform: scale(1.1);
        transform: scale(1.1);
    }
</style>