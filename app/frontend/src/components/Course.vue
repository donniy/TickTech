<template>
    <a v-on:click="pushCourse"
       class="list-ticket">
        <h3>{{course.title}}</h3>
        {{course.description}}
    </a>
</template>

<script>

export default {
    props: {
        course: Object,
            base_url: {
            type: String,
                default: "/ticket/"
            }
    },
    data: function () {
        return {};
    },
    methods: {
        pushCourse () {
            this.$router.push("/course/" + this.course.id);
        }
    }
}
</script>
