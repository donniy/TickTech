<script>
  import StudentFormLTI from './StudentFormLTI.vue'
  import StudentForm from './StudentForm.vue'

/* Load the userHome depending on the environment.
 */
export default {
    render (h) {
        return this.$lti.data.lti_session ? h(StudentFormLTI) : h(StudentForm)
    },
    components: {
        StudentFormLTI,
        StudentForm,
    },
}

</script>
