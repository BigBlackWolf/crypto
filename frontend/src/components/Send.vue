<template>
  <div class="panel panel-default">
    <div class="panel-body">
      <form @submit="onSubmit">
        <button class="btn btn-default" type="reset">
          <span class="glyphicon glyphicon-remove-circle"></span> Clear
        </button>
        <div class="form-group">
          <div class="row">
            <label class="col-sm-2 control-label"><label for="modulus">Modulus</label></label>
            <div class="col-sm-10">
              <input class="form-control" type="text" id="modulus" name="message" v-model="modulus">
            </div>
          </div>
        </div>
        <div class="form-group">
          <div class="row">
            <label class="col-sm-2 control-label"><label for="exponent">Exponent</label></label>
            <div class="col-sm-10">
              <input class="form-control" type="text" id="exponent" name="message" v-model="exponent">
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-sm-2 col-sm-offset-2">
            <input class="btn btn-success form-control" type="submit" value="Send" @click="onSubmit">
          </div>
        </div>
      </form>
      <div v-show="sign_key !== null">
        <hr>
        <div class="input-group">
          <span class="input-group-addon">Key</span>
          <input class="form-control" type="text" :value="sign_key">
        </div>
        <div class="input-group">
          <span class="input-group-addon">Signature</span>
          <input class="form-control" type="text" :value="signature">
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
        sign_key: null,
        signature: null
      }
    },
   methods: {
      onSubmit(evt) {
        evt.preventDefault();
        const payload = {
          form: {
            modulus: this.modulus,
            exponent: this.exponent
          },
          userStuff: {
            modulus: sessionStorage.getItem('modulus'),
            exponent: sessionStorage.getItem('exponent'),
            secret: sessionStorage.getItem('secret')
          }
        };
        this.getRandom(payload);
      },
      getRandom(data) {
        const path = 'http://0.0.0.0:5000/api/send';
        axios.post(path, data)
          .then(response => {
            this.sign_key = response.data.key;
            this.signature = response.data.signature;
            sessionStorage.setItem('sign_key', this.sign_key);
            sessionStorage.setItem('signature', this.signature);
          })
          .catch(error => {
            console.log(error)
          })
      }
    },
    mounted () {
      if (sessionStorage.key) {
        this.sign_key = sessionStorage.sign_key;
        this.signature = sessionStorage.signature;
      }
    }
  }
</script>
