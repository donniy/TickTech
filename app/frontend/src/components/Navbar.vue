<template>
    <nav class="navbar navbar-tiktech navbar-expand-lg">
        <router-link :to="{name: 'Home'}" class="navbar-brand">
            <img src="../assets/logo.png" class="d-inline-block align-top" width="30" height="30" alt="TikTech"> Tickets
        </router-link>
        <ul class="navbar-nav mr-auto">
            <router-link active-class="active" tag="li" :to="{name: 'UserTickets', params: {user_id: 123123123}}">
                <a class="nav-link" >My active Tickets <span class="sr-only">(current)</span></a>
            </router-link>
            <router-link active-class="active" tag="li" :to="{name: 'AskAQuestion'}">
                <a class="nav-link">Submit a ticket</a>
            </router-link>
            <router-link active-class="active" tag="li" :to="'archive'">
                <a class="nav-link">Archive</a>
            </router-link>
            <router-link active-class="active" tag="li" :to="{name: 'CourseOverview'}">
                <a class="nav-link">Course overview</a>
            </router-link>
            <router-link active-class="active" tag="li" :to="{name: 'Register'}">
                <a class="nav-link">Register</a>
            </router-link>
        </ul>
    </nav>
</template>

<script>

  export default {
      props: [],
      data: function () {
          return {};
      }
  }

</script>
