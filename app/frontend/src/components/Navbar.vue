<template>
    <nav :class="'navbar navbar-tiktech navbar-expand-md' + (transparent ? ' navbar-transparent' : '')">
        <ul class="navbar-nav mr-auto">
            <div>
                <!-- <router-link class="navbar-brand home-left navbar-buttons" to="/">Home</router-link> -->
                <ul class="breadcrumb">
                    <li class="breadcrumb-item">
                        <router-link class="breadcrumb-link" :to="( $user.logged_in() ? '/home' : '/' )">
                            Home
                        </router-link>
                    </li>
                    <li v-if="path_list.length" class="breadcrumb-item" v-for="(crumb, key) in path_list" :key="key">
                        <router-link class="breadcrumb-link" :to="crumb.path">
                            {{ crumb.meta.breadcrumb }}
                        </router-link>
                    </li>
                </ul>
            </div>
        </ul>
        <ul class="navbar-nav">
            <!-- if-else for student, supervisor (or both) and not logged in. -->
            <div v-if="(rights() & 1) === 0" class="div-inline mt-2 mt-md-0">
                <div>
                    <router-link to="/login" :class="'btn btn-primary navbar-buttons'">Login</router-link>
                    <router-link to="/register" :class="'btn btn-primary home-right navbar-buttons'">Register</router-link>
                </div>
            </div>
            <div v-else class="div-inline mt-2 mt-md-0">
              <button tag="button" style="margin-right:20px;"
                      v-if="!this.$lti.data.lti_session"
                      class="'note-add-button btn btn-primary home-right'"
                      v-on:click="$auth.logout({makeRequest: false, success: function () { $auth.token(null, '') }, redirect: '/'})">Logout</button>
            </div>
        </ul>
    </nav>
</template>

<script>
    import Vue from 'vue'
    import VueBreadcrumbs from 'vue-breadcrumbs'

    export default {
        props: ['transparent'],
        data: function () {
            return {
                path_list: []
            };
        },
        mounted: () => {
            console.log("navbar user: " + this.$user)
        },
        methods: {
            // Checks if a user is student, supervisor or both.
            rights: function () {
                // Not logged in (0), Student (3), Supervisor (5), Student & Supervisor (7)
                let perm = 0
                perm |= this.$user.logged_in()
                perm |= (this.$user.isStudent() << 1)
                perm |= (this.$user.isSupervisor() << 2)
                return perm
            },
            // Returns in which environment an user is (student: 0) (supervisor: 1)
            environment: function () {
                //  return 0
                if (this.$user.studentEnvironment == 1) {
                    return 0
                } else {
                    return 1
                }
            },
            breadcrumbList: function (to) {
                // if (this.$user.logged_in()) {
                    let matcher = this.$router.matcher.match;
                    let cur_url = '/';
                    let split_string = [];
                    let match = null;
                    let usr = this.$user.get();
                    if(typeof usr !== 'undefined') {
                        split_string = to.path.replace(':user_id', usr.id)
                        if(window.$current_course_id !== null)
                            try {
                                split_string = split_string.replace(':course_id', window.$current_course_id)
                            } catch(e) {
                                console.error(e);
                            }
                        split_string = split_string.split('/');
                    } else {
                        split_string = to.path;
                        if(window.$current_course_id !== null)
                            try {
                                split_string = split_string.replace(':course_id', window.$current_course_id)
                            } catch(e) {
                                console.error(e);
                            }
                        split_string = to.path.split('/');
                    }
                    for (let i = 0; i < split_string.length; i++) {
                        if(split_string[i] === '') continue;
                        match = matcher(cur_url + split_string[i]);
                        cur_url += split_string[i] + '/';
                        if (typeof match.name !== 'undefined' && match.name !== 'Home'
                                && match.name !== 'UserHomeLoader' && cur_url.indexOf(':course_id') === -1) {
                            if (typeof match.meta.pre !== 'undefined')
                                this.breadcrumbList({ path: match.meta.pre });
                            this.path_list.push(match);
                        }
                    }
                return
            }
            // }
        },
        watch: {
            '$route'(to, from) {
                this.path_list = [];
                this.breadcrumbList(this.$router.currentRoute)
            }
        }

    }
</script>
