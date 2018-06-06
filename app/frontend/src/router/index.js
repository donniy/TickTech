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
<<<<<<< HEAD
        path:'/courses',
        name:'CourseOverview',
        component:'CourseOverview',
=======
        path: '/user/:user_id',
        name: 'UserTickets',
        component: 'UserTickets',
>>>>>>> 14-display-tickets-of-specific-user
    },
    {
        path: '/form/',
        name: 'AskAQuestion',
        component: 'StudentForm',
    },
    {
        path: '/ta/:ta_id/inbox',
        name: 'TAInbox',
        component: 'TA_Inbox'
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
