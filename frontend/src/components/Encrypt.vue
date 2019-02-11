<template>
  <div class="panel panel-default">
    <div class="panel-body">
      <form @submit="onSubmit">
        <button class="btn btn-default" type="reset">
          <span class="glyphicon glyphicon-remove-circle"></span> Clear
        </button>
        <div class="form-group">
          <div class="row">
            <label class="col-sm-2 control-label"><label for="exponent">Modulus</label></label>
            <div class="col-sm-10">
              <input class="form-control" type="text" id="modulus" name="modulus" v-model="modulus">
            </div>
          </div>
        </div>
        <div class="form-group">
          <div class="row">
            <label class="col-sm-2 control-label"><label for="exponent">Exponent</label></label>
            <div class="col-sm-10">
              <input class="form-control" type="text" id="exponent" name="exponent" v-model="exponent">
            </div>
          </div>
        </div>
        <div class="form-group">
          <div class="row">
            <label class="col-sm-2 control-label"><label for="message">Message</label></label>
            <div class="col-sm-10">
              <input class="form-control" type="text" id="message" name="message" v-model="message">
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-sm-2 col-sm-offset-2">
            <input class="btn btn-success form-control" value="Encrypt" @click="onSubmit">
          </div>
        </div>
      </form>
      <div v-show="encrypted !== null">
        <hr>
        <div class="input-group">
          <span class="input-group-addon">Encrypted</span>
          <input class="form-control" type="text" :value="encrypted">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    data() {
      return {
        encrypted: null,
        modulus: null,
        exponent: null
      }
    },
    methods: {
      onSubmit(evt) {
        evt.preventDefault();
        const payload = {
          form: {
            modulus: this.modulus,
            exponent: this.exponent,
            message: this.message
          },
        };
        this.getRandom(payload);
      },
      getRandom(data) {
        const path = 'http://127.0.0.1:5000/api/encrypt';
        axios.post(path, data)
          .then(response => {
            this.encrypted = response.data.encrypted;
            sessionStorage.setItem('encrypted', this.encrypted);
          })
          .catch(error => {
            console.log(error)
          })
      }
    },
    mounted () {
      if (sessionStorage.modulus && sessionStorage.encrypted) {
        this.encrypted = sessionStorage.encrypted;
      }
    }
  }
</script>
