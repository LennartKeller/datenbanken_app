<template>
  <div class="box has-background-white-bis">
  <div class="card">
    <div class="card">
      <div class="card-header" v-on:click="infoBoxOpen = !infoBoxOpen">
          <p class="card-header-title">
            {{ name }}
          </p>
          <a class="card-header-icon">
            <b-icon
                :icon="infoBoxOpen ? 'menu-down' : 'menu-up'">
            </b-icon>
          </a>
      </div>
      <div class="card-content center" v-html="description" v-if="infoBoxOpen"/>
    </div>
  </div>
  <br/>
  <div class="has-background-white-bis buttons is-centered">
    <section>
      <b-field>
        <div class="field-body">
            <b-radio-button v-for="cls in classes" v-bind:key="cls" v-model="selectedClass" :native-value="cls"
                type="is-primary is-light is-outlined is-success">
                <b-icon v-if="selectedClass === cls" icon="check"></b-icon>
              <span>{{cls}}</span>
            </b-radio-button>
        </div>
      </b-field>
    </section>
    </div>
    </div>
</template>

<script>
import $backend from '../backend'

export default {
  name: 'SequenceClassificationTask',
  props: ['taskId', 'textId', 'name', 'description'],
  data () {
    return {
      config: {},
      selectedClass: null,
      error: null,
      infoBoxOpen: false
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
  created () {
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
