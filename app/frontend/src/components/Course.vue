<template>
    <a v-on:click="pushCourse" class="list-course">
        <h5>{{course.title}}</h5>
       <p style="font-size:0.8em; line-height:1;">{{course.description}}</p>
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
            return {}
        },
        methods: {
            pushCourse() {
                this.$router.push("/course/" + this.course.id)
                this.$emit('title', this.course.title)
            }
        }
    }
</script>