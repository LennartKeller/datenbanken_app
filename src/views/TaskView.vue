<template>
<div id="task-view" class="container">
  <TextBox v-bind:textId="currentTextId" :key="currentTextId"></TextBox>
  <br>
  <b-button class="button-text-control" id="button-previous" type="is-primary is-light" v-on:click="decrementCurrentId">Prev</b-button>
  <b-button class="button-text-control" id="button-next" type="is-primary is-light" v-on:click="incrementCurrentId">Next</b-button>
</div>
</template>

<script>
// import $backend from '../backend'
import TextBox from '@/views/TextBox'

export default {
  name: 'TaskView',
  components: {TextBox},
  data () {
    return {
      collectionData: {},
      currentTextId: 1
    }
  },
  methods: {
    incrementCurrentId () {
      this.currentTextId++
    },
    decrementCurrentId () {
      this.currentTextId--
    }
  }
}
</script>

<style scoped>
  .button-text-control {margin: 1em;}
</style>
