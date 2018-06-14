<template>
    <transition name="modal">
    	<div class="modal-mask">
    		<div class="modal-wrapper">
    			<div class="modal-container">

    				<div class="modal-header">
    					<slot name="header">
    						<h3>{{warning}}</h3>
    					</slot>
    				</div>

    				<div class="modal-body">
    					<slot name="body">
    						<section>
    							<!--Student name and number  -->
    							<form @submit.prevent="handleSubmit">
    								<div class="form-group">
    									<input type="hidden" name="course_id" v-model="form.course_id" />

    									<label for="email">Email address</label>
    									<input id="email" class="form-control" name="email" v-model="form.email" v-validate="'required|min:1'" type="text" placeholder="email@example.com">

    									<label for="category">Password</label>
    									<input id="password" class="form-control" name="password" v-model="form.password" v-validate="'required|min:1'" type="password">

    									<label for="pop">Pop3 settings</label>
    									<input class="form-control" id="pop" name="pop" v-model="form.pop" v-validate="'required|min:1'" type="text" placeholder="pop.example.com">

    									<label for="port">Port</label>
    									<input id="port" class="form-control" name="port" v-model="form.port" v-validate="'required|min:1'" type="text" placeholder="995">
    								</div>
    							</form>
    							<button type="submit" class="btn btn-primary" v-on:click="changeClose">
                        Submit
                    </button>
    							<button class="btn btn-primary stop-button" v-on:click="stopThread">
                        Stop
                    </button>
    							<button class="btn btn-primary close-button" @click="$emit('close')">
                        Cancel
                    </button>
    						</section>
    					</slot>
    				</div>
    			</div>
    		</div>
    	</div>
    </transition>
</template>

<script>
    export default {
    	props: ['warning'],
    	data: function() {
    		return {
    			form: {
    				email: "",
    				password: "",
    				pop: "",
    				port: "995",
    				course_id: this.$route.params.course_id
    			}
    		};
    	},
    	methods: {
    		changeClose() {
    			console.log("Model changeclose")
    			this.$parent.updateEmail(this.form);
    		},
    		stopThread() {
    			this.$parent.stopEmail(this.form);
    		}
    	},
    	beforeCreate: function() {
    		// Get the current email settings from server
    		const path = '/api/email/' + this.$route.params.course_id + '/settings'
    		this.$ajax.get(path, response => {
    			// TODO: Implement authentication on back-end to work with Canvas.
    			if (response.status == 200) {
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
    			}
    		});
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
    	display: table;
    	transition: opacity .3s ease;
    }

    .modal-wrapper {
    	display: table-cell;
    	vertical-align: middle;
    }

    .modal-container {
    	width: 600px;
    	margin: auto auto;
    	padding: 30px 30px;
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
    	margin: 20px 0;
    }

    .modal-default-button {
    	float: right;
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
