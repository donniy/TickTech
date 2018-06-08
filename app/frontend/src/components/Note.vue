<template>
    <div class="material-card note">
        <button class="btn btn-close-note" @click="showModal = true">
            <i class="material-icons"> close </i>
        </button>

        <h4> {{note.user_id}}: </h4>
        <p> {{note.text}} </p>

        <modal v-if="showModal" warning="Are you sure you want to remove this note?"
               @yes="closeNote()" @close="showModal = false"></modal>
    </div>
</template>


<script>

  import Modal from './ClosePrompt.vue'

  export default {
      props: ['note'],
      data: function () {
          return {
              showModal: false
          };
      },
      methods: {
          closeNote(){
              this.showModal = false
              // TODO:
              // Implement backend of note closing.  
          }
      },
      components: {
          'modal' : Modal
      }
  }

</script>
