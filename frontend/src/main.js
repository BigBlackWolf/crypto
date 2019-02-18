// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Generate from './components/Generate'
import Encrypt from './components/Encrypt'
import Decrypt from './components/Decrypt'
import Signature from './components/Signature'
import Verify from './components/Verify'
import Send from './components/Send'
import Receive from './components/Receive'

Vue.config.productionTip = false

Vue.component('tab-generate', {
  components: {Generate},
  template: '<Generate/>'
})
Vue.component('tab-encrypt', {
  components: {Encrypt},
  template: '<Encrypt/>'
})
Vue.component('tab-decrypt', {
	components: {Decrypt},
  template: '<Decrypt/>'
})
Vue.component('tab-signature', {
	components: {Signature},
  template: '<Signature/>'
})
Vue.component('tab-verify', {
	components: {Verify},
  template: '<Verify/>'
})
Vue.component('tab-send', {
	components: {Send},
  template: '<Send/>'
})
Vue.component('tab-receive', {
	components: {Receive},
  template: '<Receive/>'
})

new Vue({
  el: '#menu',
  data: {
    currentTab: 'Generate',
    tabs: ['Generate', 'Encrypt', 'Decrypt', 'Signature', 'Verify', 'Send', 'Receive']
  },
  computed: {
    currentTabComponent: function () {
      return 'tab-' + this.currentTab.toLowerCase()
    }}
  }
)

