<template>
    <div id="app">
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <a class="navbar-brand" href="/">
    <img src="./assets/logo.png" class="d-inline-block align-top" width="30" height="30" alt="TikTech"> Tickets
            </a>
            <ul class="navbar-nav mr-auto">
                <li class="nav-item active">
                    <a class="nav-link" href="/mytickets">My Tickets <span class="sr-only">(current)</span></a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/form">Submit a ticket</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Archive</a>
                </li>
            </ul>
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
