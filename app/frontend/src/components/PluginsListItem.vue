<template>
    <div>
        <template v-for="(plugin, pid) in plugins">
            <md-list-item>
                <span class="md-list-item-text">{{plugin.name}}</span>
                <md-switch v-model="plugin.active" @change="updatePluginState(pid)" />
            </md-list-item>
            <md-list-item @click="" v-if="plugin.active">
                <md-icon>settings</md-icon>
                <span class="md-list-item-text">Configure</span>
            </md-list-item>
        </template>
    </div>
</template>

<script>

export default {
    props: ['plugin', 'pid'],
}

</script>
