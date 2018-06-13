<template>
    <a v-bind:href="'/course/'+course.id" class="list-ticket">
    	<h3>{{course.title}}</h3> {{course.description}}
    </a>
</template>

<script>
    export default {
    	props: ['course'],
    	data: function() {
    		return {};
    	}
    }
</script>
