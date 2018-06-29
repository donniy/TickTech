<template>
<div v-if="$auth.ready()">
	<h2 class="form-header center-display">Set password</h2>
	<md-dialog-alert :md-active.sync="succes" md-content="Your password has been reset!" @click="onConfirm" md-confirm-text="Login now!" />

	<form class="md-layout center-display" v-on:submit.prevent="resetPassword">
		<md-card class="md-layout-item md-size-50 md-small-size-100">
			<md-card-content>

				<md-field>
					<label for="password">Password</label>
					<md-input id="password" name="password" v-model="form.password" v-validate="'required'" type="password" />
				</md-field>
				<md-field>
					<label for="password_confirmation">Repeat password</label>
					<md-input v-on:keyup="checkPswConfirmation" id="password_confirmation" name="password_confirmation" v-model="form.password_confirmation" v-validate="'required'" type="password" />
				</md-field>
				<div v-show="errors.has('email')" class="invalid-feedback">
					{{ errors.first('email') }}
				</div>
				<div v-show="errors.has('psw')" class="invalid-feedback">
					{{ errors.first('psw') }}
				</div>
				<div v-if="!this.pswstatus">
					Passwords do not match!
				</div>
				<p id="loginfail" class="def-error-msg" v-show="this.responseerror">
					{{this.message}}
				</p>
				<md-button class="btn btn-primary" type="submit" v-bind:disabled="errors.any()">
					Reset
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
				password: '',
				password_confirmation: ''
			},
			pswstatus: true,
			message: '',
			responseerror: false,
            succes: false
		}
	},
	methods: {
		checkPswConfirmation() {
			this.pswstatus = (this.form.password === this.form.password_confirmation) || this.form.password === ""
		},
		resetPassword() {
			let code = this.$route.query.code
			const path = '/api/user/resetpsw';
			this.$ajax.post(path, {
				code: code,
				password: this.form.password,
				psw_confirmation: this.form.password_confirmation
			}).then(response => {
                if (response.status == 200) {
                    let errormsg = response.data.json_data
    				this.message = errormsg
    				this.responseerror = true
                } else {
                    this.succes = true
                }
			}).catch(error => {
				console.log(error)
			})
		},
        onConfirm() {
            this.$router.push('/login')
        }
	},
	mounted: function() {
		if (!this.$route.query.code) {
			this.$router.back()
		}
	}
}
</script>
