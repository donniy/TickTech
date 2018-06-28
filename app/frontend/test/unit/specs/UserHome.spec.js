import { shallowMount } from '@vue/test-utils'
import UserHome from '../../../src/components/UserHome.vue'

const factory = (values = {}) => {
    return shallowMount(UserHome, {
        propsData: { ...values }
    })
}

describe(UserHome, () => {
    it('should display coures if TA', () => {
        const wrapper = factory({isTA: true})

        expect(wrapper.find('.md-elevation-5').text()).toEqual('Courses')
    })

    it('should display tickets if not TA', () => {
        const wrapper = factory()

        expect(wrapper.find('.md-elevation-5').text()).toEqual('Tickets')
    })


    
})