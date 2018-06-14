<template>
    <nav :class="'navbar navbar-tiktech navbar-expand-md' + (transparent ? ' navbar-transparent' : '')">
         <ul class="navbar-nav mr-auto">
             <div>
                <router-link class="navbar-brand home-left navbar-buttons" to="/">Home</router-link>

             </div>
         </ul>
         <ul class="navbar-nav">
             <!-- if-else for student, supervisor (or both) and not logged in. -->
             <div v-if="(rights() & 1) === 0" class="div-inline mt-2 mt-md-0">
                 <div>
                     <router-link to="/login" :class="'navbar-buttons'">Login</router-link>
                     <router-link to="/register" :class="'home-right navbar-buttons'">Register</router-link>
                 </div>
             </div>
             <!-- Student and Supervisor -->
             <div v-else-if="rights() ^ 7 === 0" class="div-inline mt-2 mt-md-0">
                 <div v-if="environment() === 0">
                     <router-link to="/login" :class="'navbar-buttons'">Switch Supervisor</router-link>
                     <button class="'btn note-add-button btn btn-primary btn-primary home-right'" type="button" v-on:click="$user.logout()">Logout</button>
                 </div>
                 <div v-else>
                     <router-link to="/" :class="'navbar-buttons'">Switch Student</router-link>
                      <button class="'btn note-add-button btn btn-primary btn-primary home-right'" type="button" v-on:click="$user.logout()">Logout</button>
                 </div>
             </div>
             <!-- Student or Supervisor -->
             <div v-else-if="rights() ^ 7 > 0" class="div-inline mt-2 mt-md-0">
                <button tag="button" class="'btn note-add-button btn btn-primary btn-primary home-right'" v-on:click="$user.logout()">Logout</button>
             </div>
         </ul>
    </nav>
</template>

<script>

  export default {
      props: ['transparent'],
      data: function () {
          return {};
      },
      mounted: () => {
          console.log("navbar user: " + this.$user)
      },
      methods: {
         // Checks if a user is student, supervisor or both.
         rights: function () {
             // Not logged in (0), Student (3), Supervisor (5), Student & Supervisor (7)
             let perm = 0;
             perm |= this.$user.logged_in();
             perm |= (this.$user.isStudent() << 1);
             perm |= (this.$user.isSupervisor() << 2);
             return perm;
         },
         // Returns in which environment an user is (student: 0) (supervisor: 1)
         environment: function() {
            //  return 0
             if (this.$user.studentEnvironment == 1) {
                 return 0
             } else {
                 return 1
             }
         },
     }

  }

</script>
