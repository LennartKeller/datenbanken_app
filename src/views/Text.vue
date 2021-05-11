<template>
<div id="text-component">
  <div id="text-box">
    <md-card md-with-hover>
      <md-ripple>
        <md-card-header>
          <div class="md-title">Card with hover effect</div>
          <div class="md-subhead">It also have a ripple</div>
        </md-card-header>
        <md-card-content>
          {{text}}
        </md-card-content>
      </md-ripple>
    </md-card>
  </div>

  <div v-on:click="toUpperCase">Groß</div>
</div>

</template>

<script>
// import $backend from '../backend'
export default {
  name: 'Text',
  data () {
    return {
      text: 'Hello World'
    }
  },
  methods: {
    toUpperCase () {
      this.text = this.text.toUpperCase()
    }
  }
}
</script>

<style scoped>

</style>
