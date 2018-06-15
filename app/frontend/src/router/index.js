import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
    {
        path: '/',
        name: 'Home',
        component: 'Home',
        meta: {
            breadcrumb: '/',
        },
    },
    {
        path: '/home',
        name: 'userhome',
        component: 'UserHome',
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
            pre: '/home'
        },
    },

    {
        path: '/user/tickets',
        name: 'UserTickets',
        component: 'UserTickets',
        meta: {
            breadcrumb: 'User Tickets'
        },
    },
    {
        path: '/ticket/submit/',
        name: 'SubmitTicket',
        component: 'StudentForm',
        meta: {
            breadcrumb: 'Create Ticket'
        },
    },
    {
        path: '/ticket/:ticket_id',
        name: 'SingleTicket',
        component: 'SingleTicket',
        meta: {
            breadcrumb: 'Ticket',
            pre: '/user/:user_id'
        },
    },
    {
        path: '/team/',
        name: 'Team',
        component: 'Team',
        meta: {
            breadcrumb: 'Team'
        },
    },
    {
        path: '/login',
        name: 'Login',
        component: 'Login',
        meta: {
            breadcrumb: 'Login'
        },
    },
    {
        path: '/register',
        name: 'Register',
        component: 'Register',
        meta: {
            breadcrumb: 'Register'
        },
    },
    {
        path: '/course/:course_id/labels',
        name: 'Labels',
        component: 'Labels',
        meta: {
            breadcrumb: 'Course Labels'
        },
    },
    {
        path: '/student/ticket/:ticket_id',
        name: 'StudentTicket',
        component: 'StudentTicket',
        meta: {
            breadcrumb: 'Student Ticket',
            pre: '/user/:user_id'
        },
    },
    {
        path: '*',
        component: 'NotFound'
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
