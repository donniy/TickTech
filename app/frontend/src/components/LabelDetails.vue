<template>
    <div>
        <h2 class="md-title">{{label.label_name}}</h2>
        <plugin :key="pid" :pid="pid" :label_id="label.label_id" :plugin="plugin" v-for="(plugin, pid) in plugins" />
        <md-subheader>Actions</md-subheader>
        <md-list-item @click="showModal = true">
            <md-icon>delete</md-icon>
            <span class="md-list-item-text">
                Delete label
            </span>
        </md-list-item>
        <md-dialog-confirm
            :md-active.sync="showModal"
            md-title="Delete label"
            :md-content="'Are you sure you want to delete label ' + label.label_name + '?'"
            md-confirm-text="Yes"
            md-cancel-text="No"
            @md-confirm="closeLabel" />
    </div>
</template>

<script>
import Modal from './ClosePrompt.vue'
import LabelDetailsPlugin from './LabelDetailsPlugin.vue'

export default {
    props: ['label'],
    data: function () {
        return {
            showModal: false,
            assignmentModal: false,
            plugins: {},
        }
    },
    methods: {
        // Remove the current selected label.
        closeLabel() {
            const path = '/api/labels/' + this.label.label_id + '/close'
            this.showModal = false
            this.$ajax.post(path, response => { })
        },
        // Retrieve all plugins for this label.
        getPlugins() {
            const path = '/api/labels/' + this.label.label_id + '/plugins'
            this.$ajax.get(path, response => {
                this.plugins = response.data.json_data
            })
        },
    },
    watch: {
        label: function() {
            this.showModal = false,
            this.getPlugins()
        }
    },
    mounted: function () {
        this.getPlugins()
    },
    components: {
        'modal': Modal,
        'plugin': LabelDetailsPlugin,
    }
}

</script>
