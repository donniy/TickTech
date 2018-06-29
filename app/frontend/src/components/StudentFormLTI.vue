<!-- StudentForm.vue creates the form to submit a ticket as a student. -->
<template>
    <div class="container">
        <div class="navbar-spacing"></div>
        <h2 class="form-header center-display">Submit a ticket</h2>
        <form class="md-layout center-display" v-on:submit.prevent="sendTicket">
            <md-card class="md-layout-item md-size-50 md-small-size-100">
                <md-card-content>

                    <md-field>
                        <label for="subject">Subject</label>
                        <md-input id="subject" v-validate="'required|max:50'" name="subject" v-model="form.subject" type="text" />
                        <div v-show="errors.has('subject')" class="invalid-feedback">
                            {{ errors.first('subject') }}
                        </div>
                    </md-field>

                    <md-field>
                        <label for="message">Message</label>
                        <md-textarea id="message" name="message" v-validate="'required'" v-model="form.message"></md-textarea>
                        <div v-if="errors.has('message')" class="invalid-feedback">
                            {{ errors.first('message') }}
                        </div>
                    </md-field>

                    <p v-on:click="addFiles()" class="file-add-text">
                        <i class="material-icons file-add-icon">attach_file</i> Add attachments (Max 10 MB, 5 files)</p>
                    <div class="large-12 medium-12 small-12 cell">
                        <input name="files" class="hidden-input" type="file" id="files" ref="files" multiple v-on:change="handleFilesUpload()" />
                    </div>
                    <div class="medium-12 small-12 cell" style="overflow-y: hidden;">
                        <div v-for="(file, key) in files" class="file-listing" style="width: 100%; text-align: left;">{{ file.name }}
                            <i v-on:click="removeFile( key )" class="material-icons file-remove-icon">delete_forever</i>
                            <hr class="light-stripe">
                        </div>
                    </div>

                    <div class="padding-left-10">
                        <p class="def-error-msg" v-show="fileTooLarge">
                            Too large a file detected
                            </br>
                        </p>
                        <p class="def-error-msg" v-show="fileTooMany">
                            Too many files detected
                            </br>
                        </p>
                    </div>

                    <md-field>
                        <label for="category">Category</label>
                        <md-select id="category" v-validate="''" md-dense v-model="form.labelid">
                            <md-option disabled value="">Label this question</md-option>
                            <md-option v-for="option in labels" v-bind:key="option.label_id" v-bind:value="option.label_id">
                                {{ option.label_name }}
                            </md-option>
                        </md-select>
                        <div class="md-helper-text">Selecting a category is optional, but can help assign your question to the right person.</div>
                    </md-field>

                    <button type="submit" class="btn btn-primary btn-block btn-lg margin-top" v-bind:disabled="errors.any()">
                        Submit
                    </button>

                    <p class="def-error-msg" v-show="errors.any()">
                        Please fill out the form correctly.
                    </p>
                </md-card-content>
            </md-card>
        </form>
    </div>
</template>

<script>


import VeeValidate from 'vee-validate'

let maxFiles = 6
let maxFileSize = 10000000 // == 10MB

export default {
    data() {
        return {
            form: {
                message: "",
                labelid: "",
                subject: "",
            },
            files: [],
            labels: [],
            courseid: "",
            fileTooLarge: false,
            fileTooMany: false,
        }
    },
    methods: {
        /*
         * Upload the supplied files.
         */
        handleFilesUpload() {
            if (this.fileTooMany || this.fileTooLarge) {
                return
            }

            let uploadedFiles = this.$refs.files.files
            if (uploadedFiles.length >= maxFiles) {
                this.fileTooMany = true
            } else {
                this.fileTooMany = false
            }

            // Adds the uploaded file to the files array
            let largeFileFound = false
            for (var i = 0; i < uploadedFiles.length; i++) {
                if (uploadedFiles[i].size > maxFileSize) {
                    this.fileTooLarge = true
                    largeFileFound = true
                }
                this.files.push(uploadedFiles[i])
            }
            if (!largeFileFound) {
                this.fileTooLarge = false
            }
        },
        /*
         * Removes the supplied files.
         */
        removeFile(key) {
            this.files.splice(key, 1)

            // Recheck the amount of files
            if (this.files.length >= maxFiles) {
                this.fileTooMany = true
            } else {
                this.fileTooMany = false
            }

            // Check the size of the files
            let largeFileFound = false
            for (var i = 0; i < this.files.length; i++) {
                if (this.files[i].size > maxFileSize) {
                    this.fileTooLarge = true
                    largeFileFound = true
                }
            }

            if (!largeFileFound) {
                this.fileTooLarge = false
            }

        },
        /*
         * Adds supplie files.
         */
        addFiles() {
            if (!this.fileTooMany && !this.fileTooLarge) {
                this.$refs.files.click()
            }
        },
        /*
         * Check if all required boxes are filled correctly.
         */
        sendTicket() {
            this.$validator.validateAll().then((result) => {
                if (result) {
                    let formData = new FormData()

                    // Add the uploaded files to the files array
                    for (var i = 0; i < this.files.length; i++) {
                        let file = this.files[i]
                        formData.append('files[' + i + ']', file)
                    }

                    // Add the rest of the form to the formdata
                    formData.append('message', this.form.message)
                    formData.append('courseid', this.courseid)
                    formData.append('labelid', this.form.labelid)
                    formData.append('subject', this.form.subject)

                    const path = '/api/ticket/submit'
                    this.$ajax.post(path, formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    })
                        .then(response => {
                            this.$router.push({
                                name: 'StudentTicket',
                                params: {
                                    ticket_id: response.data.json_data.ticketid
                                }
                            })
                            this.form = ""

                        }).catch((error) => {
                            window.alert("Something went wrong...")
                        })
                }
            })

        },

        /*
         * Get all labels in a course.
         */
        get_course_labels() {
            const pathLabels = '/api/labels/' + this.courseid;
            this.$ajax.get(pathLabels)
                .then(response => {
                    this.labels = response.data.json_data;
                }).catch(error => {

                })
        },
    },
    mounted() {
        /*
         * Verify if a user is logged in, otherwise redirect to login page.
         */
        if (!this.$user.logged_in()) {
            this.$router.push('/login')
        }
        this.courseid = this.$lti.data.lti_data['tiktech_course_id'];
        this.get_course_labels();
    }
}

</script>
