<template>
  <div>
    <h2> {{ this.title }} </h2>

    <p> Upload a csv file in the following format:
      student_id,student_name,student_email
    </p>
      <label for="file_photo" v-model="file"> {{ this.label_message }} </label>
      <input type="file" name="students_file" id="students_file" ref="student_file"
             v-on:change="attachFile()"><br>
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
    data () {
        return {
            file: null,
        }
    },
    methods: {
        // Add error to form and maybe check size.
        attachFile(e) {
            const file = this.$refs.student_file.files[0]
            console.log(file)
            if (file.name.split('.').pop() != "csv") {
                this.file = null;
                this.resetFileName();
                return
            }
            this.file = file;

        },

        submitFile() {
            if (this.file === null)
                return;

            const formData = new FormData();
            formData.append("files", this.file)
            const path = this.api_path
            this.$ajax.post(path, formData, {
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            }
            }).then(response => {
                this.file = null;
                this.resetFileName()
            })
        },
        resetFileName() {
            document.getElementById('students_file').value = "Uploaded";
        }
    }

}

</script>
