<template>
  <div class="panel panel-default">
    <div class="panel-body">
      <form @submit="onSubmit">
        <button class="btn btn-default" type="reset">
          <span class="glyphicon glyphicon-remove-circle"></span> Clear
        </button>
        <div class="form-group">
          <div class="row">
            <label class="col-sm-2 control-label">Length</label>
            <div class="col-sm-10">
              <input class="form-control" v-model="length" type="text" id="length" name="length" required>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-sm-2 col-sm-offset-2">
            <input class="btn btn-success form-control" value="Generate" @click="onSubmit">
          </div>
        </div>
      </form>
      <div v-show="modulus !== null">
        <hr>
        <div class="input-group">
          <span class="input-group-addon">Modulus</span>
          <input class="form-control" type="text" :value="modulus">
        </div>
        <div class="input-group">
          <span class="input-group-addon">Exponent</span>
          <input class="form-control" type="text" :value="exponent">
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
        modulus: null,
        exponent: null,
        length: null
      }
    },
    methods: {
      onSubmit(evt) {
        evt.preventDefault();
        const payload = {
          form: {
            length: this.length
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
        const path = 'http://127.0.0.1:5000/api/random';
        axios.post(path, data)
          .then(response => {
            this.modulus = response.data.modulus;
            this.exponent = response.data.exponent;
            sessionStorage.setItem('modulus', response.data.modulus);
            sessionStorage.setItem('exponent', response.data.exponent);
            sessionStorage.setItem('secret', response.data.secret);
          })
          .catch(error => {
            console.log(error)
          })
      }
    }
  }
</script>
