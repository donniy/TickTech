<template>
	<router-link :to="base_url + ticket.id" class="list-ticket">
		<h3>{{ticket.title}}</h3> Status: {{ticket.status.name}} - Gesteld door: {{ticket.user_id}}
	</router-link>
</template>

<script>
	export default {
		props: {
			ticket: Object,
			base_url: {
				type: String,
				default: "/ticket/"
			}
		},
		data: function () {
			return {}
		}
	}
</script>