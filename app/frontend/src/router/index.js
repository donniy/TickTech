import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
    {
        path: '/',
        name: 'Home',
        component: 'Home',
        meta: {
            breadcrumb: 'Home',
        },
    },
    {
        path:'/courses',
        name:'CourseOverview',
        component:'CourseOverview',
        meta: {
            breadcrumb: 'Course Overview'
        },
    },
    {
        path: '/home/',
        name: 'userhome',
        component: 'UserHome',
    },
    {
        path: '/course/:course_id',
        name: 'CourseTickets',
        component: 'CourseTickets',
        meta: {
            breadcrumb: 'Course',
            pre: '/courses'
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
        path: '/user/:user_id',
        name: 'UserTickets',
        component: 'UserTickets',
        meta: {
            breadcrumb: 'User Tickets'
        },
    },
    {
        path: '/form/',
        name: 'AskAQuestion',
        component: 'StudentForm',
        meta: {
            breadcrumb: 'Create Ticket'
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
        path: '/ta/:user_id',
        name: 'TAInbox',
        component: 'TA_Inbox',
        meta: {
            breadcrumb: 'Inbox'
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
        path: '/sort',
        name: 'SortingTickets',
        component: 'SortingTickets',
        meta: {
            breadcrumb: 'Sort Tickets'
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
