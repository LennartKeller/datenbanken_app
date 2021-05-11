<template>
<div id="text-component" class="container">
  <div id="text-box" class="box">
    {{text}}
  </div>
  <div v-if="error" id="error-box" class="box">
    {{error}}
  </div>
  <div v-on:click="renderText">getText</div>
</div>

</template>

<script>
import $backend from '../backend'
export default {
  name: 'TextBox',
  // props: ['textId'],
  data () {
    return {
      textData: {},
      error: null,
      textId: '2'
    }
  },
  computed: {
    'text': function () {
      if ('content' in this.textData) {
        return this.textData.content
      }
      return ''
    }
  },
  methods: {
    renderText () {
      $backend.fetchText(this.textId)
        .then(response => { this.textData = response })
        .catch(error => { this.error = error.message })
    }
  }
}
</script>

<style scoped>

</style>
