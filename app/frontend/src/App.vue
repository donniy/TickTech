<template>
    <div id="app">
        <nav class="navbar navbar-light bg-light">
            <a class="navbar-brand" href="/">
    <img src="./assets/logo.png" class="d-inline-block align-top" width="30" height="30" alt="TikTech"> Tickets
            </a>
        </nav>
        <div class="navbar-spacing"></div>
        <div class="container">
        <router-view/>
        </div>
    </div>
</template>

<script>
export default {
    name: 'App'
}
</script>
