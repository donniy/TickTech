<script>

import Tribute from "tributejs";

/* Build the tribute and config for matching.
 * DOCS: https://github.com/zurb/tribute
 * Maybe create a vuejs wrapper
 */
let defaultMention = {
    values: [
    ],
    selectTemplate: function (item) {
        return '@' + item.original.id;
    },
    lookup: function (ta) {
        return ta.name + ' ' + ta.id;
    }
}

//Source https://github.com/syropian/vue-tribute/blob/master/src/index.js
export default {
    name: 'mentions',
    props: {
        matchingData: {
            type: Array,
            required: true
        }
    },

    data: function () {
        return {
            tribute: null,
            options: defaultMention,
        }
    },

    mounted: function () {
        this.tribute = new Tribute(this.options)
        const $child_element = this.$slots.default[0].elm
        this.tribute.attach($child_element)
        this.tribute.append(0, this.matchingData)
    },
    methods: {
        /* This is needed because vue does not update the model when a match is found,
               because it does not trigger the right event. So we update the model oursels,
               because the input of the textarea is actually changed.
               Only gets executed when a match is found.
             */
        matchFound(e) {
            let text_including_full_match = document.getElementById('textAreaForNotes').value
            this.noteTextArea = text_including_full_match
        },
   },
    render(h) {
        return h(
            'div',
            {
                staticClass: 'v-tribute'
            },
            this.$slots.default
    )}
}
</script>
