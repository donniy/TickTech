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
        path: '/student',
        name: 'student',
        component: 'student',
    },
    {
        path: '/ticket/:ticket_id',
        name: 'SingleTicket',
        component: 'SingleTicket',
    },
    { // NOTE: Deze moet onderaan blijven staan! Anders krijg je altijd 404
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
