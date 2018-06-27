<template>
</template>
<script>
/*
Function that start an lti session. It gets an acess token from the
redirect function. It then checks if the access token is valid,
if the token is not valid we redirect to the login page.
If the token is valid, we authenticate the user and
redirect to the home page, with lti set to true.
*/
export default {
    methods: {
        /* Function that gets the lti sanitized lti launch data. */
        get_lti_data () {
            const path = '/api/lti/get_lti_params';
            this.$ajax.get(path).then(response => {
                this.$lti.data.lti_data = response.data.json_data;

            })
        }
    },
    mounted: function () {
        let auth_url = '/api/lti/auth_session';
        if (this.$route.query.code)
            auth_url += '?code=' + this.$route.query.code;

        this.$auth.login({
            url: auth_url,
            headers: {Authorization: 'Bearer ' + this.$route.params.access_token},
            success: function (response) {
                console.log("PARAMS")
                console.log(this.$route.query)
                if (response.data.json_data.access_token) {
                    this.$auth.token(null,
                                     response.data.json_data.access_token);
                }
                else {
                    this.$auth.authenticated = false;
                    this.$router.push('/login');
                }
                this.$auth.authenticated = true;
                this.$lti.data.lti_session = true;
                this.get_lti_data();
                this.$auth.fetch({
                    data: {},
                    success: function () {
                        console.log(this.$auth.user())
                        this.$router.push('/home');
                    },
                    error: function (response_fetch) {
                        console.error(response_fetch)
                    },
                });
            },
            error: function (response) {
                console.error(response)
                this.$router.push('/login')
            },
            rememberMe: true,
            fetchUser: false,
        })
    }
}
</script>
