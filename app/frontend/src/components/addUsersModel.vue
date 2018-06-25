<!-- addUsersModel.vue adds enrolled students to a course from a CSV file.-->
<template>
    <div>
        <h2> {{ this.title }} </h2>
        <p> Upload a csv file in the following format: student ID, student name, student email. </p>
        <label for="file_photo" v-model="file"> {{ this.label_message }} </label>
        <input type="file" name="studentsFile" id="studentsFile" ref="studentFile" v-on:change="attachFile()">
        <br>
        <input v-on:click="submitFile" type="submit" value="Upload">
    </div>
</template>

<script>
    export default {
        props: {
            title: {
                required: true
            },
            label_message: {
                required: true
            },
            api_path: {
                required: true
            },
        },
        data() {
            return {
                file: null,
            }
        },
        // TODO: Add error checking to form and maybe check size ?
        methods: {
            // Attach a csv file to upload. 
            attachFile(e) {
                const file = this.$refs.studentFile.files[0]
                if (file.name.split('.').pop() != "csv") {
                    this.file = null
                    this.resetFileName()
                    return
                }
                this.file = file
            },
            // Submit the attached file and upload. 
            submitFile() {
                if (this.file === null)
                    return

                const formData = new FormData()
                const path = this.api_path
                formData.append("files", this.file)
                this.$ajax.post(path, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }).then(response => {
                    this.file = null
                    this.resetFileName()
                })
            },
            resetFileName() {
                document.getElementById('studentsFile').value = "Uploaded"
            }
        }
    }
</script>