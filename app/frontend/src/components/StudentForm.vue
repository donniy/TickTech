<div class="columns" id="app">
    <div class="column is-two-thirds">
        <section class="section">
            <h1 class="title">Submit a question to the Mailing list</h1>

        <section class="form">
            <!--Student name and number  -->
            <form v-on:submit.prevent="$validator.validateAll(); console.log(form);">
                <div class="field">
                    <label class="label">Name and student number</label>
                    <div class="control">
                        <input name="name" v-model="form.name" v-validate="'required|min:1'" v-bind:class="{'is-danger': errors.has('name')}" class="input" type="text" placeholder="Full name">
                    </div>
                    <div class="control">
                        <input name="name" v-model="form.sudentid" v-validate="'required|min:5'" v-bind:class="{'is-danger': errors.has('studentid')}" class="input" type="number" placeholder="Student Number">
                    </div>

                    <p class="help is-danger" v-show="errors.has('name')">
                        {{ errors.first('name') }}
                    </p>
                    <p class="help is-danger" v-show="errors.has('studentid')">
                        {{ errors.first('studentid') }}
                    </p>
                </div>

                <div class="field">
                    <label class="label">Message</label>
                    <div class="control">
                        <textarea name="message" class="textarea" v-validate="'required'" placeholder="Message" v-bind:class="{'is-danger': errors.has('message')}" v-model="form.message"></textarea>
                    </div>
                    <p class="help is-danger" v-show="errors.has('message')">
                        {{ errors.first('message') }}
                    </p>
                </div>

                <div class="field">
                    <label class="label">Category</label>
                    <div class="control">
                        <div class="select">
                            <select v-model="form.label_class">
                                <option disabled value="">Nothing selected</option>
                                <option v-for="option in options.labels" v-bind:value="option.value">
                                    {{ option.text }}
                                </option>
    					    </select>
                        </div>
                    </div>
                </div>

                <div class="field is-grouped">
                    <div class="control">
                        <button v-bind:disabled="errors.any()" class="button is-primary">
    								Submit
    			        </button>
                    </div>
                </div>

            </form>
        </section>
    </section>
</div>

Vue.use(VeeValidate);

new Vue({
    el: "#app",
    data: {
        form: {
            name: "",
            studentid: "",
            message: "",
            label_class: "",
            terms: false,
            concepts: [],
            js_awesome: ""
    },
    options: {
        labels: [
            { value: "Assignment 1", text: "Ass1" },
            { value: "Assignment 2", text: "Ass2" },
            { value: "Assignment 3", text: "Ass3" },
            { value: "Deadlines", text: "Deadlines" },
            { value: "Absense", text: "Absense" },
            { value: "Course guide", text: "Course" }
            ]
        }
    }
});
