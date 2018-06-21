<template>
    <div>
        <!--Student name and number  -->
        <div class="row justify-content-around">
            <div class="col-sm-8 col-md-6">
                    <h2 class="form-header">Submit a question</h2>
                <form enctype="multipart/form-data" class="material-form" v-on:submit.prevent="sendTicket">
                    <md-avatar>
                        <i class="material-icons">
                            info
                        </i>
                            <md-tooltip md-direction="left">This page is can be used to create a ticket.
                            </br>In order to assign the right Teaching Assistant (TA) to your
                            </br>ticket please select the right corresponding course and label</md-tooltip>
                    </md-avatar>
                    <div class="form-group">
                        <label for="subject">Subject</label>
                        <input id="subject" class="form-control" v-validate="'required|max:50'" name="subject" v-model="form.subject" type="text"
                            placeholder="Question about...">
                        <div v-show="errors.has('subject')" class="invalid-feedback">
                            {{ errors.first('subject') }}
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="message">Message</label>
                        <textarea-autosize id="message" class="form-control" name="message" v-validate="'required'" placeholder="While working at the assignment, I ran into..."
                            v-model="form.message"></textarea-autosize>
                        <div v-if="errors.has('message')" class="invalid-feedback">
                            {{ errors.first('message') }}
                        </div>
                    </div>
                    <p v-on:click="addFiles()" class="file-add-text"> <i class="material-icons file-add-icon">attach_file</i> Add attachments (Max 10 MB, 5 files)</p>
                    <div class="large-12 medium-12 small-12 cell">
                        <input name="files" class="hidden-input" type="file" id="files" ref="files" multiple v-on:change="handleFilesUpload()"/>
                    </div>
                    <div class="file-name-container medium-12 small-12 cell">
                        <div v-for="(file, key) in files" class="file-listing"">{{ file.name }} <i v-on:click="removeFile( key )" class="material-icons file-remove-icon">delete_forever</i><hr class="light-stripe"></div>
                    </div>

                    <p class="def-error-msg" v-show="fileTooLarge">
                        Too large a file detected
                    </br>
                    </p>
                    <p class="def-error-msg" v-show="fileTooMany">
                        Too many files detected
                    </br>
                    </p>
                    <div class="form-group">
                        <label for="course">Course</label>
                        <select id="course" v-validate="'required'" class="form-control custom-select" v-model="form.courseid">
                            <option  disabled value="">Please select a course</option>
                            <option v-for="obj in categories.courses" v-bind:key="obj.id" v-bind:value="obj.id">
                                {{ obj.title }}
                            </option>
                        </select>

                    </div>
                    <div class="form-group">
                        <label for="category">Category</label>
                        <select id="category" v-validate="''" class="form-control custom-select" v-model="form.labelid">
                            <option disabled value="">Label this question</option>
                            <option v-for="option in categories.labels[form.courseid]" v-bind:key="option.label_id" v-bind:value="option.label_id">{{ option.label_name }}</option>
                        </select>
                        <small class="form-text">Selecting a category is optional, but can help assign your question to the right person.</small>
                    </div>

                    <button type="submit" class="btn btn-primary btn-block btn-lg" v-bind:disabled="errors.any()">
                        Submit
                    </button>

                    <p class="def-error-msg" v-show="errors.any()">
                        Please fill out the form correctly
                    </p>

                </form>

            </div>
        </div>

        <infomodal v-if="showModal" @close="showModal = false">
        </infomodal>
    </div>
</template>

<script>

import VeeValidate from 'vee-validate'

let maxFiles = 6
let maxFileSize = 10000000 // 10mb

export default {
    data() {
        return {
            form: {
                message: "",
                courseid: "",
                labelid: "",
                subject: "",
            },
            files: [],
            categories: {
                courses: [],
                labels: {}
            },
            fileTooLarge : false,
            fileTooMany : false,
        }
    },
    computed: {
        options: function(event) {
            return categories.labels[form.courseid]
        }
    },
    methods: {
        handleFilesUpload(){
            if (this.fileTooMany || this.fileTooLarge) {
                return
            }

            let uploadedFiles = this.$refs.files.files;
            if (uploadedFiles.length >= maxFiles) {
                this.fileTooMany = true
            } else {
                this.fileTooMany = false
            }

            // Adds the uploaded file to the files array
            let largeFileFound = false
            for( var i = 0; i < uploadedFiles.length; i++ ){
                if (uploadedFiles[i].size > maxFileSize) {
                    this.fileTooLarge = true
                    largeFileFound = true
                }
                this.files.push( uploadedFiles[i] );
            }
            if (!largeFileFound) {
                this.fileTooLarge = false
            }
        },
        removeFile( key ){
            this.files.splice( key, 1 );

            // Recheck the amount of files
            if (this.files.length >= maxFiles) {
                this.fileTooMany = true
            } else {
                this.fileTooMany = false
            }

            // Check the size of the files
            let largeFileFound = false
            for( var i = 0; i < this.files.length; i++ ){
                if (this.files[i].size > maxFileSize) {
                    this.fileTooLarge = true
                    largeFileFound = true
                }
            }
            if (!largeFileFound) {
                this.fileTooLarge = false
            }

        },
        addFiles(){
            if (!this.fileTooMany && !this.fileTooLarge) {
                this.$refs.files.click();
            }
        },
        sendTicket() {
            this.$validator.validateAll().then((result)=>
            {
                if (result) {

                    // Create a formdata object
                    let formData = new FormData();

                    // Add the uploaded files to the files array
                    for( var i = 0; i < this.files.length; i++ ){
                        let file = this.files[i];
                        formData.append('files[' + i + ']', file);
                    }

                    // Add the rest of the form to the formdata
                    formData.append('message', this.form.message)
                    formData.append('courseid', this.form.courseid)
                    formData.append('labelid', this.form.labelid)
                    formData.append('subject', this.form.subject)

                    const path = '/api/ticket/submit'
                    this.$ajax.post(path, formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    })
                    .then(response => {
                        console.log(response)
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

        }
    },
    mounted() {
        if (!this.$user.logged_in()) {
            this.$router.push('/login')
        }

        const pathLabels = '/api/labels'
        const pathCourses = '/api/courses'

        this.$ajax.get(pathCourses)
            .then(response => {
                for (let i = 0; i < response.data.json_data.length; i++) {
                    let dataObj = response.data.json_data[i]
                    this.categories.courses.push(dataObj)
                }
                for (let i = 0; i < this.categories.courses.length; i++) {
                    let courseid = this.categories.courses[i].id
                    let currLabelPath = pathLabels + '/' + courseid
                    this.$ajax.get(currLabelPath)
                        .then(response => {
                            this.categories.labels[courseid] = response.data.json_data
                            console.log(this.categories.labels[courseid])
                        }).catch(error => {
                            console.log(error)
                        })
                }

            }).catch(error => {
                console.log(error)
            });
        // for (let i = 0; i < this.categories.courses.length; i++) {
        //     //axios_csrf.get(pathLabels + '/' + this.courses[i].course_id)
        //     console.log("HELLO")
        //     console.log(this.categories.courses[i].course_id)
        // }
        this.$ajax.get(pathLabels)
            .then(response => {
                console.log
                for (let i = 0; i < response.data.json_data.length; i++) {
                    let elem = response.data.json_data[i]
                    if (this.categories.labels[elem.course_id])
                        this.categories.labels[elem.course_id].push({
                            value: elem.name,
                            text: elem.name
                        });
                    else
                        this.categories.labels[elem.course_id] = [{
                            value: elem.name,
                            text: elem.name
                        }]
                }
            }).catch(error => {
                console.log(error)
            })
        }
    }

</script>
