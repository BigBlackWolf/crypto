<template>
  <div class="panel panel-default">
    <div class="panel-body">
      <form @submit="onSubmit">
        <button class="btn btn-default" type="reset">
          <span class="glyphicon glyphicon-remove-circle"></span> Clear
        </button>
        <div class="form-group">
          <div class="row">
            <label class="col-sm-2 control-label"><label for="ciphertext">Ciphertext</label></label>
            <div class="col-sm-10">
              <input class="form-control" type="text" id="ciphertext" name="ciphertext" v-model="ciphertext">
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-sm-2 col-sm-offset-2">
            <input class="btn btn-success form-control" value="Decrypt" @click="onSubmit">
          </div>
        </div>
      </form>
      <div v-show="decrypted !== null">
        <hr>
        <div class="input-group">
          <span class="input-group-addon">Decrypted</span>
          <input class="form-control" type="text" :value="decrypted">
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
        decrypted: null
      }
    },
    methods: {
      onSubmit(evt) {
        evt.preventDefault();
        const payload = {
          form: {
            ciphertext: this.ciphertext
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
        const path = 'http://0.0.0.0:5000/rsa/api/decrypt';
        axios.post(path, data)
          .then(response => {
            this.decrypted = response.data.decrypted;
            sessionStorage.setItem('decrypted', this.decrypted);
          })
          .catch(error => {
            console.log(error)
          })
      }
    },
    mounted () {
      if (sessionStorage.decrypted) {
        this.decrypted = sessionStorage.decrypted;
      }
    }
  }
</script>
