<template>
    <md-list-item v-on:click="pushCourse">
        <div class="md-list-item-text">
            <h5>{{course.title}}</h5>
            <h6>{{course.name}}</h6>
            <p>{{course.description}}</p>
        </div>
    </md-list-item>
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

            /*
             * Go to the selected course page.
             */
            pushCourse() {
                this.$router.push("/course/" + this.course.id)
                this.$emit('title', this.course.title)
            }
        }
    }
</script>
