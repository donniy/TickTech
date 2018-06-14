<template>
    <div>
        <div id="LoginMain">
            <section>
                <h1>Login to our fantastic messaging service</h1>

                <div id ="LoginInput">
                    <!-- Login functionaliteit voor testing -->
                    <div class="form-group">
                        <input type="text" name="username" v-model="input.username" placeholder="Username" style="center" />
                    </div>
                    <div class="form-group">
                        <input type="password" name="password" v-model="input.password" placeholder="Password" style="center" />
                    </div>
                    <div class="form-group">
                        <button style="border-radius: 4px" class="btn btn-primary" type="button" v-on:click="login()">Login</button>
                    </div>
                </div>
            </section>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'Login',
        data() {
            return {
                input: {
                    username: "",
                    password: ""
                }
            }
        },
        methods: {
            login() {
                if(this.input.username != "" && this.input.password != "") {
                    if(this.input.username == this.$parent.mockAccount.username && this.input.password == this.$parent.mockAccount.password) {
                        this.$emit("authenticated", true);
                        this.$router.replace({ name: "secure" });
                    } else {
                        console.log("The username and / or password is incorrect");
                    }
                } else {
                    console.log("A username and password must be present");
                }
            }
        }
    }
</script>

<style scoped>
    #LoginMain {
        width: 80%;
        background-color: #FFFFFF;
        padding: 20px;
    }
    #LoginInput {
        padding-top: 5%;
        padding-bottom: 5%;
        padding-left: 5%;
        padding-right: 18%;
        align-content: center;
    }
</style>
