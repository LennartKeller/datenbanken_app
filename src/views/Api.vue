<template>
  <div class="about">
    <h1>Backend Resources Demo</h1>
    <h1 style="color: red;">Test</h1>
    <p>Click on the links below to fetch data from the Flask server</p>
    <a href="" @click.prevent="fetchResource">Fetch</a><br/>
    <a href="" @click.prevent="fetchSecureResource">Fetch Secure Resource</a><br/>
    <a href="" @click.prevent="fetchTestResource">Test</a>
    <h4>Results</h4>
    <p v-for="r in resources" :key="r.timestamp">
      Server Timestamp: {{r.timestamp | formatTimestamp }}
    </p>
    <p style="color: red;" v-for="resp in test" :key="resp.hello">
      Nerv: {{resp}}

    </p>
    <p>{{error}}</p>
  </div>
</template>

<script>
/**
 * Dummy component for debugging.
 */
import $backend from '../backend'

export default {
  name: 'about',
  data () {
    return {
      resources: [],
      test: [],
      error: ''
    }
  },
  methods: {
    fetchResource () {
      $backend.fetchResource()
        .then(responseData => {
          this.resources.push(responseData)
        }).catch(error => {
          this.error = error.message
        })
    },
    fetchSecureResource () {
      $backend.fetchSecureResource()
        .then(responseData => {
          this.resources.push(responseData)
        }).catch(error => {
          this.error = error.message
        })
    },
    fetchTestResource () {
      $backend.fetchTestResource()
        .then(responseData => {
          this.test.push(responseData)
        }).catch(error => {
          this.error = error.message
        })
    }
  }
}

</script>

<style lang="scss">
</style>
