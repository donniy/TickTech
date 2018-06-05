<template>
    <div>
        <div class="vertical-menu">
            <a href="#" class="active">Home</a>
            <a href="#">My Tickets</a>
            <a href="#">Submit a Ticket</a>
            <a href="#">Archive</a>
        </div>
    </div>
</template>

<style scoped>
.vertical-menu {
    float: left;
    width: 200px; /* Set a width if you like */
}

.vertical-menu a {
    background-color: #ffffff; /* Grey background color */
    color: black; /* Black text color */
    display: block; /* Make the links appear below each other */
    padding: 12px; /* Add some padding */
    text-decoration: none; /* Remove underline from links */
    border-radius: 8px;
}

.vertical-menu a:hover {
    background-color: #ccc; /* Dark grey background on mouse-over */
}

.vertical-menu a.active {
    background-color: #CA0033; /* Add a green color to the "active/current" link */
    color: white;
}
</style>