import { shallowMount, mount } from '@vue/test-utils'
import Label from '../../../src/components/Label.vue'
import Labels from '../../../src/components/Labels.vue'

const labelFactory = (values = {}) => {
    return mount(Label, {
        propsData: { ...values  }
    })
}

const factory = (methods = {}, data = {}) => {
    return mount(Labels, {
        methods: { ...methods  },
        data: () => {return {...data}}
    })
}

describe('Labels.vue', () => {
    it('sets the correct default data', () => {
        expect(typeof Label.data).to.equal('function')
    })

    it('shows a label when it is added added', () => {
        const mockedLabels = [
            {label_name: "test label"},
        ]

        const getCourseStub = sinon.stub()
        const getLabelsStub = sinon.stub()

        const wrapper = factory({
            getCourse: getCourseStub,
            getLabels: getLabelsStub
        }, {
            course: {title: "unknown"}
        })

        wrapper.setData({labels: mockedLabels})

        expect(wrapper.html()).to.contain("test label")
    })

    it('shows labels when multiple are added', () => {
        const mockedLabels = [
            {label_name: "test label a"},
            {label_name: "test label b"},
        ]

        const getCourseStub = sinon.stub()
        const getLabelsStub = sinon.stub()

        const wrapper = factory({
            getCourse: getCourseStub,
            getLabels: getLabelsStub
        }, {
            course: {title: "unknown"}
        })

        wrapper.setData({labels: mockedLabels})

        expect(wrapper.html()).to.contain("test label a")
        expect(wrapper.html()).to.contain("test label b")
    })
})
