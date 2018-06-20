import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
    {
        path: '/',
        name: 'Home',
        component: 'Home',
        meta: {
            breadcrumb: '/',
            auth: false
        },
    },
    {
        path: '/home',
        name: 'userhome',
        component: 'UserHome',
        meta: {
            breadcrumb: 'Home',
            auth: true
        }
    },
    {
        path: '/homer',
        name: 'userhomer',
        component: 'UserHomer',
        meta: {
            breadcrumb: 'Home'
        }
    },
    {
        path: '/course/:course_id',
        name: 'CourseTickets',
        component: 'CourseTickets',
        meta: {
            breadcrumb: 'Course',
            pre: '/home',
            auth: true
        },
    },

    {
        path: '/user/tickets',
        name: 'UserTickets',
        component: 'UserTickets',
        meta: {
            breadcrumb: 'User Tickets',
            auth: true
        },
    },
    {
        path: '/ticket/submit/',
        name: 'SubmitTicket',
        component: 'StudentForm',
        meta: {
            breadcrumb: 'Create Ticket',
            auth: true
        },
    },
    {
        path: '/ticket/:ticket_id',
        name: 'SingleTicket',
        component: 'SingleTicket',
        meta: {
            breadcrumb: 'Ticket',
            pre: '/user/:user_id',
            auth: true
        },
    },
    {
        path: '/team/',
        name: 'Team',
        component: 'Team',
        meta: {
            breadcrumb: 'Team',
            auth: false
        },
    },
    {
        path: '/login',
        name: 'Login',
        component: 'Login',
        meta: {
            breadcrumb: 'Login',
            auth: false
        },
    },
    {
        path: '/register',
        name: 'Register',
        component: 'RegisterForm',
        meta: {
            breadcrumb: 'Register',
            auth: false
        },
    },
    {
        path: '/course/:course_id/labels',
        name: 'Labels',
        component: 'Labels',
        meta: {
            breadcrumb: 'Course Labels',
            auth: true
        },
    },
    {
        path: '/student/ticket/:ticket_id',
        name: 'StudentTicket',
        component: 'StudentTicket',
        meta: {
            breadcrumb: 'Student Ticket',
            pre: '/user/:user_id',
            auth: true
        },
    },
    {
        path: '*',
        component: 'NotFound',
        meta: {
            auth: true
        }
    }
]

const routes = routerOptions.map(route => {
    return {
        ...route,
        component: () => import(`@/components/${route.component}.vue`)
    }
})

Vue.use(Router)

export default new Router({
    routes,
    mode: 'history'
})
