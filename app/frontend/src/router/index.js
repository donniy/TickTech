import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
    {
        path: '/',
        name: 'Home',
        component: 'Home',
        meta: {
            breadcrumb: '/',
            auth: undefined
        },
    },
    {
        path: '/home',
        name: 'UserHome',
        component: 'UserHome',
        meta: {
            breadcrumb: 'Home',
            auth: true
        }
    },
    {
        path: '/course/:course_id',
        name: 'CourseTickets',
        component: 'CourseTickets',
        meta: {
            breadcrumb: 'Course',
            pre: '/home',
            auth: ['supervisor', 'ta']
        },
    },

    {
        path: '/user/tickets',
        name: 'UserTickets',
        component: 'UserTickets',
        meta: {
            breadcrumb: 'User Tickets',
            auth: ['student']
        },
    },
    {
        path: '/ticket/submit/',
        name: 'SubmitTicket',
        component: 'StudentForm',
        meta: {
            breadcrumb: 'Create Ticket',
            pre: '/home',
            auth: ['student']
        },
    },
    {
        path: '/ticket/:ticket_id',
        name: 'SingleTicket',
        component: 'SingleTicket',
        meta: {
            breadcrumb: 'Ticket',
            pre: '/course/:course_id',
            auth: true
        },
    },
    {
        path: '/team/',
        name: 'Team',
        component: 'Team',
        meta: {
            breadcrumb: 'Team',
            auth: undefined
        },
    },
    {
        path: '/login',
        name: 'Login',
        component: 'Login',
        meta: {
            breadcrumb: 'Login',
            auth: undefined
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
            auth: ['supervisor', 'ta']
        },
    },
    {
        path: '/student/ticket/:ticket_id',
        name: 'StudentTicket',
        component: 'StudentTicket',
        meta: {
            breadcrumb: 'Student Ticket',
            pre: '/user/:user_id',
            auth: ['student']
        },
    },
    {
        path: '*',
        component: 'NotFound',
        meta: {
            auth: undefined
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
