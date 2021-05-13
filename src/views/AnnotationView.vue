<template>
  <div id="task-view" class="container">
    <TextBox v-bind:textId="currentTextId" :key="currentTextId" ref="textBox"></TextBox>
    <SequenceClassificationTask
        v-for="(t, idx) in sequenceClassificationTasks"
        :key="t.id.toString() + currentTextId.toString()"
        :task-id="t.id"
        :text-id="currentTextId"
        :ref="'task-' + idx.toString()"
    />
    <br>

    <b-message v-if="error !== null" type="is-danger" has-icon>{{ error }}</b-message>
    <!--
    <b-button class="button-text-control" id="button-previous" type="is-primary is-light" v-on:click="onClickPrevious">
      Prev
    </b-button>
    <b-button class="button-text-control" id="button-next" type="is-primary is-light" v-on:click="onClickNext">Next
    </b-button>
    -->
    <b-button v-on:click="onClickDiscard" class="button-text-control" type="is-danger" outlined>
       <b-icon pack="fas" icon="times-circle" size="is-small"></b-icon>
      <span>Discard</span>
    </b-button>
    <b-button v-on:click="onClickSubmit" class="button-text-control" type="is-success" outlined>
      <b-icon pack="fas" icon="check-circle" size="is-small"></b-icon>
      <span>Submit</span>
    </b-button>
  </div>
</template>

<script>
import $backend from '../backend'
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
      taskList: [],
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
    /* onClickPrevious () {
      if (this.checkTaskStates()) {
        this.decrementCurrentId()
      }
    },
    onClickNext () {
      if (this.checkTaskStates()) {
        this.incrementCurrentId()
      }
    }, */
    onClickDiscard () {
      this.discardText()
        .then(() => {
          this.error = null
          this.incrementCurrentId()
        })
    },
    onClickSubmit () {
      if (this.checkTaskStates()) {
        this.incrementCurrentId()
      }
    },
    allTasksFinished () {
      let states = []
      for (let key in this.$refs) {
        if (key.startsWith('task-')) {
          states.push(this.$refs[key][0].isFinished())
        }
      }
      return states.every(elem => elem)
    },
    getTasks () {
      $backend.fetchTasksOfCollection(this.collectionId)
        .then(response => {
          this.taskList = response
        })
        .catch(error => {
          this.error = error
        })
    },
    discardText () {
      return $backend.discardText(this.currentTextId)
        .then(response => { console.log(response.success) })
        .catch(error => { this.error = error })
    }
  },
  computed: {
    sequenceClassificationTasks: function () {
      return this.taskList.filter(task => task.type === 'SequenceClassification')
    }
  },
  beforeMount () {
    this.getTasks()
  }
}
</script>

<style scoped>
.button-text-control {
  margin: 1em;
}
</style>
