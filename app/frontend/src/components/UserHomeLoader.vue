<script>
import UserHomeLTI from './UserHomeLTI.vue'
import UserHome from './UserHome.vue'

/* Load the userHome depending on the environment.
 */
export default {
    render (h) {
        return this.$lti.data.lti_session ? h(UserHomeLTI) : h(UserHome)
    },
    components: {
        UserHome,
        UserHomeLTI,
    },
}

</script>
