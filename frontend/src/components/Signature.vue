<template>
  <div class="panel panel-default">
    <div class="panel-body">
      <form @submit="onSubmit">
        <button class="btn btn-default" type="reset">
          <span class="glyphicon glyphicon-remove-circle"></span> Clear
        </button>
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
            <input class="btn btn-success form-control" type="submit" value="Create" @click="onSubmit">
          </div>
        </div>
      </form>
      <div v-show="signature !== null">
        <hr>
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
        signature: null
      }
    },
   methods: {
      onSubmit(evt) {
        evt.preventDefault();
        const payload = {
          form: {
            message: this.message
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
        const path = 'http://0.0.0.0:5000/rsa/api/sign';
        axios.post(path, data)
          .then(response => {
            this.signature = response.data.signature;
            sessionStorage.setItem('signature', this.signature);
          })
          .catch(error => {
            console.log(error)
          })
      }
    },
    mounted () {
      if (sessionStorage.signature) {
        this.signature = sessionStorage.signature;
      }
    }
  }
</script>
