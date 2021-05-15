<template>
  <div class="container is-vcentered">
    <section class="column">
      <b-field>
            <b-radio-button v-for="cls in classes" v-bind:key="cls" v-model="selectedClass" :native-value="cls"
                type="is-primary is-light is-outlined">
                <b-icon v-if="selectedClass === cls" icon="check"></b-icon>
                <span>{{cls}}</span>
            </b-radio-button>
      </b-field>
    </section>
  </div>
</template>

<script>
import $backend from '../backend'

export default {
  name: 'SequenceClassificationTask',
  props: ['taskId', 'textId'],
  data () {
    return {
      config: {},
      selectedClass: null,
      error: null
    }
  },
  computed: {
    finished: function () {
      return this.selectedClass !== null
    },
    classes: function () {
      return this.config.classLabels
    }
  },
  methods: {
    getTaskConfig () {
      $backend.fetchSequenceClassificationTaskConfig(this.taskId)
        .then(response => { this.config = response })
        .catch(error => { this.error = error.message })
    },
    submit () {
      let annotation = {
        class: this.selectedClass
      }
      $backend.postSequenceClassificationAnnotation(annotation, this.textId, this.taskId)
        .then(response => { console.log(response.success) })
        .catch(error => { this.error = error })
    },
    isFinished () {
      return this.selectedClass !== null
    }
  },
  beforeMount () {
    this.getTaskConfig()
  },
  beforeDestroy () {
    /* if (this.selectedClass !== null) {
      this.submit()
    } */
  }
}
</script>

<style scoped>

</style>
