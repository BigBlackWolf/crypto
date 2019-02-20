<template>
  <div class="panel panel-default">
    <div class="panel-body">
      <form @submit="onSubmit">
        <button class="btn btn-default" type="reset">
          <span class="glyphicon glyphicon-remove-circle"></span> Clear
        </button>
        <div class="form-group">
          <div class="row">
            <label class="col-sm-2 control-label"><label for="exponent">Signature</label></label>
            <div class="col-sm-10">
              <input class="form-control" type="text" id="signature" name="exponent" v-model="signature">
            </div>
          </div>
        </div>
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
            <label class="col-sm-2 control-label"><label for="key">Key</label></label>
            <div class="col-sm-10">
              <input class="form-control" type="text" id="key" name="message" v-model="key">
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-sm-2 col-sm-offset-2">
            <input class="btn btn-success form-control" value="Verify" @click="onSubmit">
          </div>
        </div>
      </form>
      <div v-show="key2 !== null">
        <hr>
        <div class="input-group">
          <span class="input-group-addon">Key</span>
          <input class="form-control" type="text" :value="key2">
        </div>
        <div class="input-group">
          <span class="input-group-addon">Verified</span>
          <input class="form-control" type="text" :value="verified2">
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
        verified2: null,
        key2: null
      }
    },
    methods: {
      onSubmit(evt) {
        evt.preventDefault();
        const payload = {
          form: {
            key: this.key,
            modulus: this.modulus,
            exponent: this.exponent,
            signature: this.signature
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
        const path = 'http://0.0.0.0:5000/api/receive';
        axios.post(path, data)
          .then(response => {
            this.key2 = response.data.key;
            this.verified2 = response.data.signature;
            sessionStorage.setItem('key2', this.key2);
            sessionStorage.setItem('verified2', this.verified2);
          })
          .catch(error => {
            console.log(error)
          })
      }
    },
    mounted () {
      if (sessionStorage.key) {
        this.key2 = sessionStorage.key2;
        this.verified2 = sessionStorage.verified2;
      }
    }
  }
</script>
