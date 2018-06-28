<template>
    <div>
        <md-subheader>{{plugin.name}}</md-subheader>
        <md-list-item>
            <md-icon>settings</md-icon>
            <span class="md-list-item-text">
                Active
            </span>
            <md-switch @change="updatePluginState" v-model="plugin.active" />
        </md-list-item>
        <md-list-item class="md-inset" v-if="plugin.active" @click="showModal = true">
            <div class="md-list-item-text">
                <span>
                    Assignment ID: {{plugin.assignment_id}}
                </span>
                <span class="md-text-primary">
                    Click to change
                </span>
            </div>
            <md-dialog-prompt
                :md-active.sync="showModal"
                v-model="plugin.assignment_id"
                md-title="Assignment ID"
                md-input-placeholder="Fill in the ID"
                md-confirm-text="Save"
                @md-confirm="updateAssignmentID"/>
        </md-list-item>
    </div>
</template>

<script>

export default {
    props: ['plugin', 'pid', 'label_id'],
    data: function() {
        return {
            showModal: false
        }
    },
    methods: {
        updatePluginState() {
            if (this.plugin.active) {
                this.activatePlugin()
            } else {
                this.deactivatePlugin()
            }
        },
        activatePlugin() {
            console.log("Activate " + this.plugin.name)
            console.log(this.plugin)
            const path = '/api/labels/' + this.label_id + '/plugins'
            this.$ajax.post(path, {plugin_id: this.pid}, response => {
                //
            })
        },
        deactivatePlugin() {
            console.log("Deactivate " + this.plugin.name)
            const path = '/api/labels/' + this.label_id + '/plugins/' + this.pid
            this.$ajax.delete(path, {}, response => {
                //
            })
        },
        updateAssignmentID(val) {
            const path = '/api/labels/' + this.label_id + '/plugins/' + this.pid
            this.$ajax.put(path, {assignment_id: val}, response => {
                //
            })
        }
    }
}

</script>
