<template>
<div v-if="$auth.ready()">
	<h2 class="form-header center-display">Reset password</h2>

	<form class="md-layout center-display" v-on:submit.prevent="setResetCode">
		<md-card class="md-layout-item md-size-50 md-small-size-100">
			<md-card-content>
				<md-field>
					<label for="email">Email address</label>
					<md-input autofocus id="email" name="email" v-model="form.email" v-validate="'required'" type="email" />
				</md-field>
				<div v-show="errors.has('email')" class="invalid-feedback">
					{{ errors.first('email') }}
				</div>
				<md-button class="btn btn-primary" type="submit" v-bind:disabled="errors.any()">
					Request reset link
				</md-button>
				<p id="loginfail" class="def-error-msg" v-show="this.forgotstatus">
					{{this.message}}
				</p>
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
				email: '',
			},
			forgotstatus: false,
			message: '',
		}
	},
	methods: {
		// Log the student in.
		setResetCode() {
			this.$validator.validateAll().then((result) => {
				const path = '/api/user/setresetcode';
				this.$ajax.post(path, {
					email: this.form.email
				}, response => {
					if (response.status == 201) {
						this.$router.push('/login')
					} else {
						console.log(response.data.json_data)
						this.message = response.data.json_data
						this.forgotstatus = true
					}
				})
			})
		}
	}
}
</script>
