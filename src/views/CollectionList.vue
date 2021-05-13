<template>
  <div>
    <section class="hero">
  <div class="hero-body">
    <p class="title">
      Collections
    </p>
  </div>
</section>
    <div id="collection-list" class="container">
      <div class="card" v-for="collection in collectionList" :key="collection.id">
        <router-link :to="{name: 'annotation-view', params: {collectionId: collection.id}}">
          <header class="card-header">
            <p class="card-header-title">
             {{collection.name}}
            </p>
          </header>
        </router-link>
      </div>
    </div>
    <b-message v-if="error !== null" type="is-danger" has-icon>{{error}}</b-message>
  </div>
</template>

<script>
import $backend from '@/backend'

export default {
  name: 'CollectionList',
  data () {
    return {
      collectionList: null,
      error: null
    }
  },
  methods: {
    getCollectionList () {
      $backend.fetchCollectionList()
        .then(response => { this.collectionList = response })
        .catch(error => { this.error.messagge = error })
    }
  },
  beforeMount () {
    this.getCollectionList()
  }
}
</script>

<style scoped>

</style>
