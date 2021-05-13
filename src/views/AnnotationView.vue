<template>
<div id="task-view" class="container">
  <TextBox v-bind:textId="currentTextId" :key="currentTextId" ref="textBox"></TextBox>
  <SequenceClassificationTask :key="currentTextId + 'task'" ref="task-0"/> <!-- Hacky-->
  <SequenceClassificationTask :key="currentTextId + 'task1'" ref="task-1"/>
  <br>
  <b-message v-if="error !== null" type="is-danger" has-icon>{{error}}</b-message>
  <b-button class="button-text-control" id="button-previous" type="is-primary is-light" v-on:click="onClickPrevious">Prev</b-button>
  <b-button class="button-text-control" id="button-next" type="is-primary is-light" v-on:click="onClickNext">Next</b-button>
</div>
</template>

<script>
// import $backend from '../backend'
import TextBox from '@/views/TextBox'
import SequenceClassificationTask from '@/views/SequenceClassificationTask'

export default {
  name: 'AnnotationView',
  props: ['collectionId'],
  components: {SequenceClassificationTask, TextBox},
  data () {
    return {
      collectionData: {},
      currentTextId: 1,
      error: null
    }
  },
  methods: {
    incrementCurrentId () {
      this.currentTextId++
    },
    decrementCurrentId () {
      this.currentTextId--
    },
    checkTaskStates () {
      this.error = null
      if (!this.allTasksFinished()) {
        this.error = 'Not all Tasks are finished.'
        return false
      }
      return true
    },
    onClickPrevious () {
      if (this.checkTaskStates()) {
        this.decrementCurrentId()
      }
    },
    onClickNext () {
      if (this.checkTaskStates()) {
        this.incrementCurrentId()
      }
    },
    allTasksFinished () {
      let states = []
      for (let key in this.$refs) {
        if (key.startsWith('task-')) {
          console.log(states)
          states.push(this.$refs[key].finished)
        }
      }
      return states.every(elem => elem)
    }
  },
  computed: {

    taskIds: function () {
      return [1, 2].forEach(elem => this.currentTextId + 'Task-' + elem)
    }
  }
}
</script>

<style scoped>
  .button-text-control {margin: 1em;}
</style>
