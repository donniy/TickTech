<template>
    <nav class="navbar navbar-tiktech navbar-expand-md">
         <ul class="navbar-nav mr-auto">
             <div>
                 <a class="navbar-brand home-left" href="home">Home</a>
             </div>
         </ul>
         <ul class="navbar-nav">
             <!-- if-else for student, supervisor (or both) and not logged in. -->
             <div v-if="rights() == 0" class="div-inline mt-2 mt-md-0">
                 <div>
                     <router-link to="/login">Login</router-link>
                     <router-link to="/register" :class="'home-right'">Register</router-link>
                 </div>
             </div>
             <!-- Student and Supervisor -->
             <div v-else-if="rights() == 1" class="div-inline mt-2 mt-md-0">
                 <div v-if="environment() == 0">
                     <router-link to="/login">Switch Supervisor</router-link>
                     <router-link to="/" :class="'home-right'">Logout</router-link>
                 </div>
                 <div v-else>
                     <router-link to="/">Switch Student</router-link>
                     <router-link to="/":class="'home-right'">Logout</router-link>
                 </div>
             </div>
             <!-- Student or Supervisor -->
             <div v-else-if="rights() > 1" class="div-inline mt-2 mt-md-0">
                 <router-link to="/":class="'home-right'">Logout</router-link>
             </div>
         </ul>
    </nav>
</template>

<script>

  export default {
      props: [],
      data: function () {
          return {};
      },
      mounted: function () {
          console.log("navbar user: " + this.$user)
      },
      methods: {
         // Checks if a user is student, supervisor or both.
         rights: function () {
             return 1
             // Not logged in (0), Student & Supervisor (1), Student (2), Supervisor (3).
             if ($user.loggedIn() == false) {
                 return 0
             } else {
                 if ($user.isStudent() == true) {
                     if ($user.isSupervisor() == true) {
                         return 1
                     } else {
                         return 2
                     }
                 } else {
                     return 3
                 }
             }
             return 0
         },
         // Returns in which environment an user is (student: 0) (supervisor: 1)
         environment: function() {
             return 0
             if ($user.studentEnvironment() == true) {
                 return 0
             } else {
                 return 1
             }
         }
     }

  }

</script>
