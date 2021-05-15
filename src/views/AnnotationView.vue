<template>
  <div id="task-view" class="container">
    <b-message v-if="success" type="is-success" has-icon>Collection finished!</b-message>
    <div id="tools" v-if="!success">
      <TextBox v-if="currentTextId !== null" v-bind:textId="currentTextId" :key="currentTextId" ref="textBox"></TextBox>
      <SequenceClassificationTask
          v-if="currentTextId !== null"
          v-for="(t, idx) in sequenceClassificationTasks"
          :key="t.id.toString() + currentTextId.toString()"
          :task-id="t.id"
          :text-id="currentTextId"
          :ref="'task-' + idx.toString()"
      />
      <br>
      <p v-on:click="submitAllTasks">Submit</p>
      <p>{{currentTextId}}</p>
      <b-message v-if="error !== null" type="is-danger" has-icon>{{ error }}</b-message>
      <div v-if="currentTextId !== null">
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
      success: false
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
      this.currentTextId = this.nextTextIds.pop()
      console.log(this.currentTextId)
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
        .catch(error => { this.error = error.error })
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
