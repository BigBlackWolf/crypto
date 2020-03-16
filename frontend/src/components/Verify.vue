<template>
  <div class="panel panel-default">
    <div class="panel-body">
      <form id="form">
        <button class="btn btn-default" type="reset">
          <span class="glyphicon glyphicon-remove-circle"></span> Clear
        </button>
        <div v-for="field in fields" class="form-group">
          <div class="row">
            <label class="col-sm-2 control-label">{{ field }}</label>
            <div class="col-sm-10">
              <input class="form-control" type="text" :name="field" required>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-sm-2 col-sm-offset-2">
            <input class="btn btn-success form-control" value="Generate" @click="onSubmit">
          </div>
        </div>
      </form>
      <div v-show="verified !== null">
        <hr>
        <div class="input-group">
          <span class="input-group-addon">Encrypted</span>
          <input class="form-control" type="text" :value="verified">
        </div>
      </div>
    </div>
  </div>
</template>

<style>
  label {
    text-transform: capitalize;
  }
</style>

<script>
  import axios from 'axios'

  export default {
    props: ['fields'],
    data() {
      return {
        verified: null,
      }
    },
    methods: {
      onSubmit(evt) {
        const formData = new FormData(document.getElementById('form'));
        console.log(formData);
        evt.preventDefault();
        this.getRandom(formData);
      },
      getRandom(data) {
        const path = 'http://0.0.0.0:5000/rsa/api/verify';
        axios.post(path, data)
          .then(response => {
            this.verified = response.data.verified;
            sessionStorage.setItem('verified', this.verified);
          })
          .catch(error => {
            console.log(error)
          })
      }
    },
    mounted () {
      if (sessionStorage.verified) {
        this.verified = sessionStorage.verified;
      }
    }
  }
</script>
