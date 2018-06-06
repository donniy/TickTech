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
        path: '/form/',
        name: 'AskAQuestion',
        component: 'StudentForm',
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
