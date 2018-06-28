<template>
    <md-list-item @click="clickLabel" v-if="exists">
        <span class="md-list-item-text">{{label.label_name}}</span>

        <md-dialog  :md-active.sync="showModal">
            <md-dialog-title>Do you want to remove this label?</md-dialog-title>
            <md-dialog-actions>
                <md-button class="md-primary" @click="showModal = false">Nope</md-button>
                <md-button class="md-primary" @click="closeLabel()">Yes I'm sure</md-button>
            </md-dialog-actions>
        </md-dialog>
    </md-list-item>
</template>

<script>
import Modal from './ClosePrompt.vue'

export default {
    props: ['label'],
    data: function () {
        return {
            showModal: false,
            exists: true,
            isSelected: false
        }
    },
    methods: {
        // Remove the current selected label.
        closeLabel() {
            const path = '/api/labels/' + this.label.label_id + '/close'
            this.showModal = false
            this.exists = false
            this.$ajax.post(path, response => { })
            this.$parent.getLabels()
        },
        // Change selection of labels based on mouseclick.
        clickLabel() {
            this.$emit('label-selected')
        },
        // Select current label.
        selectLabel() {
            const path = '/api/labels/' + this.label.label_id + '/select'
            this.$ajax.post(path, { user_id: this.$user.get().id })
            this.isSelected = true
        },
        // Deselect current label.
        deselectLabel() {
            const path = '/api/labels/' + this.label.label_id + '/deselect'
            this.$ajax.post(path, { user_id: this.$user.get().id })
            this.isSelected = false
        },
        // Check what labels are selected.
        checkSelected() {
            const path = '/api/labels/' + this.label.label_id + '/selected'
            this.$ajax.post(path, { user_id: this.$user.get().id }, response => {
                this.isSelected = response.data.json_data.bool
            })
        }
    },
    mounted: function () {
        this.checkSelected()
    },
    components: {
        'modal': Modal
    }
}

</script>
