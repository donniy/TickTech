<template>
    <div>
        <div class="label">
            <button class="btn removeLabel" @click="showModal = true">
                <i class="material-icons"> close </i>
            </button>

            <button class="label-name" v-bind:class="{'label-name-selected': isSelected}" data-toggle="tooltip" @click="clickLabel" title="Select to receive tickets from this label ">
                <h3>{{label.label_name}}</h3>
            </button>
        </div>

        <modal v-if="showModal" warning="Are you sure you want to remove this label?" @yes="closeLabel()" @close="showModal = false"></modal>
    </div>
</template>

<script>
    import Modal from './ClosePrompt.vue'

    export default {
        props: ['label'],
        data: function () {
            return {
                showModal: false,
                isSelected: false
            }
        },
        methods: {
            closeLabel() {
                const path = '/api/labels/' + this.label.label_id + '/close'
                this.$ajax.post(path, response => { this.showModal = false })
                this.$parent.getLabels()
            },
            clickLabel() {
                if (this.isSelected)
                    this.deselectLabel()
                else
                    this.selectLabel()
            },
            selectLabel() {
                const path = '/api/labels/' + this.label.label_id + '/select'
                this.$ajax.post(path, { user_id: this.$user.get().id })
                this.isSelected = true
            },
            deselectLabel() {
                const path = '/api/labels/' + this.label.label_id + '/deselect'
                this.$ajax.post(path, { user_id: this.$user.get().id })
                this.isSelected = false
            },
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