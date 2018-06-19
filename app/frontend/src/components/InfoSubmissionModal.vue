<template>
    <transition name="modal">
        <div class="modal-mask">
            <div class="modal-wrapper">
                <div class="modal-container">
                    <div class="modal-body">
                        <slot name="body">
                        <h1>Ticket Submission</h1>

                        <div class="row">
                            <p>This page is can be used to create a ticket. Use this form to ask a question or remark on
                            an assignment or exam. </p>
                            
                            <p>Use the subject input to specify the question and use the message
                            input to provide more information. In order to assign the right Teacher Assistant (TA) to your
                            ticket please select the corresponding course. To futher help us assign the right TA to you ticket
                            it is possible to add a label. For example this label could be the name of the assignment or
                            exam.</p>

                            <p>For futher questions about ticket submission please e-mail us at: test@test.com </p>
                        </div>  
                        
                        <div class="row buttom">
                            <div class="col-sm-4"></div>
                            <div class="col-sm-4 subheading-middle">
                                <button class="btn btn-primary close-button" @click="$emit('close')">
                                    Close
                                </button>
                            </div>
                            <div class="col-sm-4"></div>
                        </div>
                        </slot>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script>

    export default {
        data: function () {
            return {

            };
        },
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
        display: inline-table;
        transition: opacity .3s ease;
    }

    .modal-wrapper {
        display: table-cell;
        vertical-align: middle;
    }

    .modal-container {
        width: 50%;
        margin: auto auto;
        padding: auto auto;
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
        /* margin: 20px 0; */
        overflow-y: auto;
        padding: 50px 50px;
    }

    .modal-default-button {
        float: right;
    }

    .modal-stop-button {
        float: left;
    }

    .close-button {
        margin-top: 40px;
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
</style>