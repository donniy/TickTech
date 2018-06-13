<template>
    <div>
        <div class="label">
            <button class="btn removeLabel" @click="showModal = true">
                <i class="material-icons"> close </i>
            </button>

            <button class="labelText" data-toggle="tooltip"
                    title="Select to receive tickets from this label ">
                <h3>{{label.label_name}}</h3>
            </button>
        </div>

        <modal v-if="showModal" warning="Are you sure you want to remove this label?"
               @yes="closeLabel()" @close="showModal = false"></modal>
    </div>
</template>

<script>

    import axios from 'axios'
    import Modal from './ClosePrompt.vue'

    const axios_csrf = axios.create({
      headers: {'X-CSRFToken': csrf_token}
    });

  export default {
      props: ['label'],
      data: function () {
          return {
              showModal: false
          };
      },
      methods: {
          closeLabel() {
              const path = '/api/labels/' + this.label.label_id + '/close'
              this.$ajax.post(path, response => {this.showModal = false})
              this.$parent.getLabels()
          }
      },
      components: {
          'modal' : Modal
      }
  }

</script>
