<template>
<div id="text-component" class="container">
  <div id="text-box" class="box" v-html="text">
  </div>
  <div v-if="error" id="error-box" class="box">
    {{error}}
  </div>
</div>

</template>

<script>
import $backend from '../backend'
export default {
  name: 'TextBox',
  props: ['textId'],
  data () {
    return {
      textData: {},
      error: null,
      loading: null
    }
  },
  computed: {
    'text': function () {
      if ('content' in this.textData) {
        return this.textData.content
      }
      return ''
    },
    'index': function () {
      if ('index' in this.textData) {
        return this.textData.index
      }
      return null
    }
  },
  methods: {
    renderText () {
      $backend.fetchText(this.textId)
        .then(response => { this.textData = response })
        .catch(error => { this.error = error.message })
      return true
    }
  },
  beforeMount () {
    this.renderText()
  }
}
</script>

<style scoped>

</style>
