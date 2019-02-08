

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
