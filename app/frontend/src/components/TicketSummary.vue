<template>
  <transition name="modal">
    <div class="summary-container">
       <button class="btn btn-primary close-button" @click="$emit('close')">
       x</button>
      <div class="summary-tab">
      <h3>Beschrijving</h3>
      </div>
      <div class="summary-tab">
      <h3>Chat</h3>
      </div>
      <div class="summary-tab">
      <h3>Notities</h3>
      </div>
    </div>
  </transition>
</template>

<script>
  import Message from './Message.vue'

const axios_csrf = axios.create({
  headers: {'X-CSRFToken': csrf_token}
});

  export default {
      data: function () {
          return {};
      },
      method: {
        getMessages () {
            const path = '/api/ticket/' + this.$route.params.ticket_id + '/messages'
            axios.get(path)
            .then(response => {
                this.messages = response.data.json_list
            })
            .catch(error => {
                console.log(error)
            })
        },
        mounted: function () {
          this.getMessages()
          this.$socket.emit('join-room', {room: 'ticket-messages-' + this.$route.params.ticket_id})
        }
      }
    }

</script>

<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, .5);
  display: table;
  transition: opacity .3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 300px;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
  transition: all .3s ease;
  font-family: Helvetica, Arial, sans-serif;
}

.modal-header h3 {
  margin-top: 0;
  color: #42b983;
}

.modal-body {
  margin: 20px 0;
}

.modal-default-button {
  float: right;
}

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter {
  opacity: 0;
}

.modal-leave-active {
  opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}

.summary-container {
  background-color: grey;
  overflow: hidden;
}

.summary-tab{
  width: 30%;
  float: left;
}
</style>
