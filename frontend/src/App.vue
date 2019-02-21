<template>
  <div id="app">
    <nav class="navbar navbar-inverse lead">
      <div class="container">
        <div class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li class="nav-item active">
              <a class="nav-link" href="/">RSA<span class="sr-only">(current)</span></a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Cesar</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container">
      <h2 id="test">Crypto</h2>
    </div>
    <div class="container" id="menu">
      <div class="col-xs-2">
        <ul class="nav nav-pills nav-stacked" role="tablist">
          <li class="nav-item" v-for="tab in tabs" v-on:click="currentTab = tab">
            <a href="#" role="tab" v-bind:class="['nav-link', { active: currentTab === tab }]">{{ tab }}</a>
          </li>
        </ul>
      </div>
      <div class="col-xs-9 col-xs-offset-1">
        <component class="tab"
                   :is="currentTabComponent"
                   :fields="fields[currentTabComponent]">
        </component>
      </div>
    </div>
  </div>
</template>
<script>
  import Generate from './components/Generate'
  import Encrypt from './components/Encrypt'
  import Decrypt from './components/Decrypt'
  import Signature from './components/Signature'
  import Verify from './components/Verify'
  import Send from './components/Send'
  import Receive from './components/Receive'

  export default {
    components: {
      'tab-generate': Generate,
      'tab-encrypt': Encrypt,
      'tab-decrypt': Decrypt,
      'tab-signature': Signature,
      'tab-verify': Verify,
      'tab-send': Send,
      'tab-receive': Receive,
    },
    data() {
      return {
        currentTab: 'Generate',
        tabs: ['Generate', 'Encrypt', 'Decrypt', 'Signature', 'Verify', 'Send', 'Receive'],
        fields: {
          'tab-generate': ['length'],
          'tab-encrypt': ['modulus', 'exponent', 'message'],
          'tab-decrypt': ['ciphertext'],
          'tab-signature': ['message'],
          'tab-verify': ['signature', 'modulus', 'exponent', 'message'],
          'tab-send': ['modulus', 'exponent'],
          'tab-receive': ['signature', 'modulus', 'exponent', 'key']
        }
      }
    },
    computed: {
      currentTabComponent: function () {
        return 'tab-' + this.currentTab.toLowerCase()
      }
    }
  }
</script>

