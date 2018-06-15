<template>

  <div>
    <b-button class="dashboard-button" v-on:click="studentView">
      students
    </b-button>
    <b-button class="dashboard-button">
      teaching assistants
    </b-button>
    <b-button class="dashboard-button" v-on:click="emailSettings">
      email settings
    </b-button>
    <emodal v-if="showEmailModal"
            warning="Setup a fetcher to your mailinglist."
            @close="showEmailModal = false">
    </emodal>

  </div>

</template>


<script>

  import EmailModal from './EmailSettingsModal.vue'



export default {
    data () {
        return {
            showEmailModal: false,

        }
    },

    methods: {
        emailSettings() {
            this.showEmailModal = true
        },
        updateEmail(form) {
            this.showEmailModal = false
            console.log(form)
            const path = '/api/email'
            this.$ajax.post(path, form, response => {
                // TODO: Implement authentication on back-end to work with Canvas.
                console.log(response)
            })
        },
        studentView() {
            this.$router.push('/course/' + this.$route.params.course_id + '/students')
        },
    },
    components: {
        'emodal': EmailModal,
    },

}


</script>
