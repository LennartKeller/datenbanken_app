<template>
  <div class="column is-vcentered">
    <section class="column">
      <b-field position="is-centered">
            <b-radio-button v-for="cls in classes" v-bind:key="cls" v-model="selectedClass" :native-value="cls"
                type="is-primary is-light is-outlined">
                <b-icon v-if="selectedClass === cls" icon="check"></b-icon>
                <span>{{cls}}</span>
            </b-radio-button>
      </b-field>
    </section>
    <p>{{selectedClass}}</p>
  </div>
</template>

<script>
export default {
  name: 'SequenceClassificationTask',
  data () {
    return {
      classes: ['1', '2'],
      selectedClass: null
    }
  },
  computed: {
    finished: function () {
      return this.selectedClass !== null
    }
  }
}
</script>

<style scoped>

</style>
