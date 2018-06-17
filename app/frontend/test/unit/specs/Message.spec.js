import { shallowMount } from '@vue/test-utils'
import Message from '../../../src/components/Message.vue'

const factory = (values = {}) => {
  return shallowMount(Message, {
    propsData: { ...values  }
  })
}

describe('Message.vue', () => {
    it('sets the correct default data', () => {
        expect(typeof Message.data).to.equal('function')
    })

    it('should render message.text as its text content', () => {
        // Extend the component to get the constructor, which we can then initialize directly.
        const wrapper = factory({
            message: {
                text: 'Hello World',
                user_id: 123123123,
                user_name: 'Test persoon',
                type: 0,
            },
            user: {
                id: 234234234
            }
        })

        expect(wrapper.find('.message-text').text()).to.equal('Hello World')
    })

    it('should render message.user_name as its sender if message is from another user', () => {
        const wrapper = factory({
            message: {
                text: 'Hello World',
                user_id: 123123123,
                user_name: 'Test persoon',
                type: 0,

            },
            user: {
                id: 234234234
            }
        })

        expect(wrapper.find('.message-sender').text()).to.equal('Test persoon')
    })

    it('should render "You" as its sender if message is from yourself', () => {
        const wrapper = factory({
            message: {
                text: 'Hello World',
                user_id: 123123123,
                type: 0,

            },
            user: {
                id: 123123123
            }
        })

        expect(wrapper.find('.message-sender').text()).to.equal('You')
    })
})
