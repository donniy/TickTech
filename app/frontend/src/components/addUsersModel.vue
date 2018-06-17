<template>
  <div>
    <h2> Add students to this course </h2>

    <p> Upload a csv file in the following format:
      [student_id],[student_name],[student_email]
    </p>
      <label for="file_photo" v-model="file">Students:</label>
      <input type="file" name="students_file" id="students_file" refs="student_file"
             v-on:change="uploadFile($event)"><br>
      <input v-on:click="submitFile" type="submit" value="Upload">
  </div>


</template>



<script>

export default {
    data () {
        return {
            file: null,
        }
    },
    methods: {
        uploadFile(e) {
            console.log(e);
        },

        submitFile() {

        }
    }

}

</script>
