import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
    {
        path: '/',
        name: 'home',
        component: 'Home',
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
    },
    {
        path: '/mytickets/',
        name: 'mytickets',
        component: 'mytickets',
    },
    {
        path: '/user/tickets',
        name: 'UserTickets',
        component: 'UserTickets',
    },
    {
        path: '/ticket/submit/',
        name: 'SubmitTicket',
        component: 'StudentForm',
    },
    {
        path: '/ticket/:ticket_id',
        name: 'SingleTicket',
        component: 'SingleTicket',
    },
    {
        path: '/team/',
        name: 'Team',
        component: 'Team',
    },
    {
        path: '/login',
        name: 'Login',
        component: 'Login'
    },
    {
        path: '/register',
        name: 'Register',
        component: 'Register'
    },
    {
        path: '/course/:course_id/labels',
        name: 'Labels',
        component: 'Labels'
    },
    {
        path: '/student/ticket/:ticket_id',
        name: 'StudentTicket',
        component: 'StudentTicket',
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
