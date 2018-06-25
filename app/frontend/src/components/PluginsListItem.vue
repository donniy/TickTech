<template>
    <div>
        <md-list-item>
            <span class="md-list-item-text">{{plugin.name}}</span>
            <md-switch v-model="plugin.active" @change="updatePluginState(pid)" />
        </md-list-item>
        <md-list-item @click="trigger_modal" v-if="plugin.active">
            <md-icon>settings</md-icon>
            <span class="md-list-item-text">Configure {{plugin.settingsModal}}</span>
        </md-list-item>
        <md-dialog :md-active.sync="showModal">
            <md-dialog-title>{{plugin.name}} Settings</md-dialog-title>
            <md-dialog-content md-dynamic-height>
                <md-field v-for="(props, setting) in settings">
                    <label>{{ props.display_name }}</label>
                    <md-input v-model="settings[setting].value"></md-input>
                    <span class="md-helper-text">{{ props.help_text }}</span>
                </md-field>
            </md-dialog-content>
            <md-dialog-actions>
                <md-button class="md-primary" @click="showModal = false">Close</md-button>
                <md-button class="md-primary" @click="save">Save</md-button>
            </md-dialog-actions>
        </md-dialog>
    </div>
</template>

<script>

export default {
    data() {
        return {
            showModal: false,
            settings: null,
            setting_values: {},
        }
    },
    props: ['plugin', 'pid'],
    methods: {
        save: function() {
            this.showModal = false
            const path = '/api/courses/' + this.$route.params.course_id + '/plugins/' + this.pid
            let tmp = {}
            for (let key of Object.keys(this.settings)) {
                tmp[key] = this.settings[key].value
            }
            this.$ajax.put(path, tmp, response => {
                console.log(response)
            })
        },
        trigger_modal: function() {
            if (this.settings === null) {
                this.get_settings()
            }
            this.showModal = true
        },
        get_settings: function() {
            const path = '/api/courses/' + this.$route.params.course_id + '/plugins/' + this.pid
            this.$ajax.get(path, response => {
                this.settings = response.data.json_data
            })
        },
        updatePluginState() {
            const path = '/api/courses/' + this.$route.params.course_id + '/plugins/' + this.pid
            this.$ajax.patch(path, {active: this.plugin.active}, response => {
                //
            })
        },
    }
}

</script>

<style lang="scss" scoped>
  .md-dialog {
    max-width: 768px;
    width: 100%;
  }
</style>
