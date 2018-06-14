<template>
    <section>
    	<h1>Login</h1>

    	<section>
    		<!--Student name and number  -->
    		<form v-on:submit.prevent="checkUser">
    			<div class="form-group">
    				<label for="studentnumber">Student number</label>
    				<input class="form-control" id="studentnumber" name="studentnumber" v-model="form.username" v-validate="'required'" type="number" placeholder="Student Number">
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
    					const path = '/auth';
    					this.$ajax.post(path, {
    						username: this.form.username,
    						password: "JWT is cool!!!"
    					}, response => {
    						// TODO: Implement authentication on back-end to work with Canvas.
    						this.$cookies.set('token', response.data.access_token);
    						this.form.username = '';
    						this.$ajax.get('/api/user/retrieve', response => {

    							let params = this.$route.params;
    							let url = '/courses';
    							if (typeof params !== 'undefined' && typeof params.prev_url !== 'undefined')
									url = params.prev_url;
								console.log(response.data.json_data)
								if (this.$user.set(response.data.json_data.user)){
									this.$router.replace(url);
								}
    							else
    								console.log("Can\'t set user.");
    						})
    					});
    				}
    			});
    		}
    	}
    }
</script>

<style lang="scss" scoped>

</style>
