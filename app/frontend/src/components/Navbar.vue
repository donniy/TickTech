<template>
    <nav class="navbar navbar-tiktech navbar-expand-lg">
    	<div class="container">
    		<router-link :to="{name: 'Home'}" class="navbar-brand">
    			<img src="../assets/logo.jpg" class="d-inline-block align-top" width="auto" height="30" alt="TikTech">
    		</router-link>
    		<ul class="navbar-nav mr-auto">
    			<router-link active-class="active" tag="li" :to="{name: 'UserTickets', params: {user_id: 123123123}}">
    				<a class="nav-link">My active Tickets <span class="sr-only">(current)</span></a>
    			</router-link>
    			<router-link active-class="active" tag="li" :to="{name: 'AskAQuestion'}">
    				<a class="nav-link">Submit a ticket</a>
    			</router-link>
    			<router-link active-class="active" tag="li" :to="'archive'">
    				<a class="nav-link">Archive</a>
    			</router-link>
    			<router-link active-class="active" tag="li" :to="{name: 'CourseOverview'}">
    				<a class="nav-link">Course overview</a>
    			</router-link>
    		</ul>
    		<ul class="navbar-nav">
    			<router-link :v-if="$user == null" active-class="active" tag="li" :to="{name: 'Login'}">
    				<a class="nav-link">Log in</a>
    			</router-link>
    		</ul>
    	</div>
    </nav>
</template>

<script>
    export default {
    	props: [],
    	data: function() {
    		return {};
    	},
    	mounted: function() {
    		console.log("navbar user: " + this.$user)
    	}
    }
</script>
