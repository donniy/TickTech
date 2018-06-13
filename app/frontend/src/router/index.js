import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
    {
        path: '/',
        name: 'Home',
        component: 'Home',
    },
    {
        path: '/course/:course_id',
        name: 'CourseTickets',
        component: 'CourseTickets',
    },
    {
        path: '/mytickets/',
        name: 'mytickets',
        component: 'mytickets',
    },
    {
        path: '/ticket/:ticket_id',
        name: 'SingleTicket',
        component: 'SingleTicket',
    },
    {
        path: '/user/:user_id',
        name: 'UserTickets',
        component: 'UserTickets',
    },
    {
        path:'/courses',
        name:'CourseOverview',
        component:'CourseOverview',
    },
    {
        path: '/form/',
        name: 'AskAQuestion',
        component: 'StudentForm',
    },
    // {
    //     path: '/ticket/:ticket_id/closeticket',
    //     name: 'closeticket',
    //     component: 'modal'
    // },
    {
        path: '/login',
        name: 'Login',
        component: 'Login'
    },
    {
        path: '/course/:course_id/labels',
        name: 'Labels',
        component: 'Labels'
    },
    {
        path: '/ta/:ta_id',
        name: 'TAInbox',
        component: 'TA_Inbox'
    },
    {
        path: '/student/ticket/:ticket_id',
        name: 'StudentTicket',
        component: 'StudentTicket',
    },
    {
        path: '/sort',
        name: 'SortingTickets',
        component: 'SortingTickets'
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
