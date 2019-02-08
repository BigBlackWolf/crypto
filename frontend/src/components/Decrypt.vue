<template>
  <div class="panel panel-default">
    <div class="panel-body">
      <form method=post>
        <button class="btn btn-default" type="reset">
          <span class="glyphicon glyphicon-remove-circle"></span> Clear
        </button>
        <div class="form-group">
          <div class="row">
            <label class="col-sm-2 control-label"><label for="ciphertext">Ciphertext</label></label>
            <div class="col-sm-10">
              <input class="form-control" type="text" id="ciphertext" name="ciphertext">
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-sm-2 col-sm-offset-2">
            <input class="btn btn-success form-control" type="submit" value="Decrypt">
          </div>
        </div>
      </form>
      <hr>
      <div class="input-group">
        <span class="input-group-addon">Modulus</span>
        <input class="form-control" type="text">
      </div>
      <div class="input-group">
        <span class="input-group-addon">Exponent</span>
        <input class="form-control" type="text">
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    data() {
      return {
        randomNumber: null
      }
    },
    methods: {
      getRandom() {
        const path = 'http://127.0.0.1:5000/api/random'
        axios.get(path)
          .then(response => {
            this.randomNumber = response.data.number
          })
          .catch(error => {
            console.log(error)
          })
      }
    },
    created() {
      this.getRandom()
    }
  }
</script>
