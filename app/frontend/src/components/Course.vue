<template>
    <md-list-item v-on:click="pushCourse">
        <div class="md-list-item-text">
            <p class="md-subheading">{{course.title}}</p>
            <p class="md-caption">{{course.description}}</p>
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
