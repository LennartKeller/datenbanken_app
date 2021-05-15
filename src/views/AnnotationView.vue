<template>
  <div id="task-view" class="container">
    <b-message v-if="finished" type="is-success" has-icon>Collection finished!</b-message>
    <div id="tools" v-if="!finished && currentTextId !== null">
      <TextBox v-if="currentTextId !== null" v-bind:textId="currentTextId" :key="currentTextId" ref="textBox"></TextBox>
      <br>
      <SequenceClassificationTask
          v-if="!finished && currentTextId !== null"
          v-for="(t, idx) in sequenceClassificationTasks"
          :key="t.id.toString() + currentTextId.toString()"
          :task-id="t.id"
          :text-id="currentTextId"
          :name="t.name"
          :description="t.description"
          :ref="'task-' + idx.toString()"
      />
      <br>
      <b-message v-if="error !== null" type="is-danger" has-icon>{{ error }}</b-message>
      <div v-if="!finished && currentTextId !== null">
        <b-button v-on:click="onClickDiscard" class="button-text-control" type="is-danger" outlined>
           <b-icon pack="fas" icon="times-circle" size="is-small"></b-icon>
          <span>Discard</span>
        </b-button>
        <b-button v-on:click="onClickSubmit" class="button-text-control" type="is-success" outlined>
          <b-icon pack="fas" icon="check-circle" size="is-small"></b-icon>
          <span>Submit</span>
        </b-button>
      </div>
    </div>
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
      nextTextIds: [],
      currentTextId: null,
      taskList: [],
      error: null,
      finished: false
    }
  },
  methods: {
    checkTaskStates () {
      this.error = null
      if (!this.allTasksFinished()) {
        this.error = 'Not all Tasks are finished.'
        return false
      }
      return true
    },
    popCurrentTextId () {
      console.log(this.currentTextId)
      if (this.nextTextIds.length > 0) {
        this.currentTextId = this.nextTextIds.pop()
      }
      return null
    },
    onClickDiscard () {
      this.discardText()
        .then(() => {
          this.error = null
          if (this.nextTextIds.length === 0) {
            this.getNextTextIds()
              .then(() => this.popCurrentTextId())
          } else {
            this.popCurrentTextId()
          }
        })
    },
    onClickSubmit () {
      if (this.checkTaskStates()) {
        this.error = null
        this.submitAllTasks()
          .then(() => {
            if (this.nextTextIds.length === 0) {
              this.getNextTextIds()
                .then(() => this.popCurrentTextId())
                .catch((error) => { console.log(error) })
            } else {
              this.popCurrentTextId()
            }
          })
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
    },
    getNextTextIds () {
      return $backend.fetchNextTextIds(this.collectionId)
        .then(response => { this.nextTextIds = this.nextTextIds.concat(response) })
        .catch(error => {
          // Maybe this can be handled in a more elegant way...
          if (error.response.data.finished === true) {
            this.finished = true
          }
        })
    },
    submitAllTasks () {
      return new Promise(resolve => {
        let taskComponents = Object.keys(this.$refs)
          .filter(key => key.startsWith('task-'))
          .reduce((obj, key) => {
            obj[key] = this.$refs[key]
            return obj
          }, {})
        console.log(taskComponents)
        Object.entries(taskComponents).forEach(([taskRef, taskComp]) => taskComp[0].submit())
        resolve()
      })
    }
  },
  computed: {
    sequenceClassificationTasks: function () {
      return this.taskList.filter(task => task.type === 'SequenceClassification')
    }
  },
  created () {
    this.getNextTextIds()
      .then(() => { this.popCurrentTextId() })
    this.getTasks()
  }
}
</script>

<style scoped>
.button-text-control {
  margin: 1em;
}
</style>
