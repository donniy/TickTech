<!-- Label.vue implements everything label-related, such as selecting, adding and removing them. -->
<template>
    <div>
        <md-subheader>{{label.label_name}}</md-subheader>
        <md-list-item>
            <span class="md-list-item-text">
                Een optie
            </span>
            <md-switch v-model="label.bla" />
            </md-list-item>
    </div>
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
        // Retrieve all plugins for this label.
        getPlugins() {
            const path = '/api/labels/' + this.label.label_id + '/plugins'
            this.$ajax.get(path, response => {
                console.log(response.data.json_data)
            })
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
