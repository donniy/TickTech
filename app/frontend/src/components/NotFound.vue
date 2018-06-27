<template>
    <div>
        <h1 v-if="$router.currentRoute.path === '/403'">
            403 - Access forbidden for this user.
            <br />
            You will be redirected back in {{this.timeout / 1000}} seconds.
        </h1>
        <h1 v-else>404 - Page not found. </h1>
    </div>
</template>

<script>
export default {
    data() {
        return {
            timeout: 3000,
        }
    },
    mounted: function () {
        if (this.$router.currentRoute.path === '/403')
            setTimeout(() => {
                this.$router.go(-2);
            }, this.timeout);
    }
}
</script>
