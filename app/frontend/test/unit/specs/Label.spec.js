import { shallowMount, mount } from '@vue/test-utils'
import Label from '../../../src/components/Label.vue'

// const factory = (values = {}) => {
//     return mount(Label, {
//         propsData: { ...values  },
//         methods: {
//             checkSelected: function () {return}
//         }
//     })
// }

// describe('Label.vue', () => {
//     it('sets the correct default data', () => {
//         expect(typeof Label.data).to.equal('function')
//         expect( Label.data().showModal).to.equal(false)
//     })
//
//     it('should render the name of the label', () => {
//         const wrapper = factory({
//             label: {
//                 label_name: "test label"
//             }
//         })
//
//         expect(wrapper.find('.label-name').text()).to.equal('test label')
//     })
//
//     it('should not show the modal when the delete button is not clicked', () => {
//         const wrapper = factory({
//             label: {
//                 label_name: "test label"
//             }
//         })
//
//         expect(wrapper.html()).not.to.contain("Are you sure you want to remove this label")
//     })
//
//     it('should show a modal when the delete button is clicked', () => {
//         const wrapper = factory({
//             label: {
//                 label_name: "test label"
//             }
//         })
//
//         wrapper.find('.removeLabel').trigger('click')
//
//         expect(wrapper.html()).to.contain("Are you sure you want to remove this label")
//     })
// })
