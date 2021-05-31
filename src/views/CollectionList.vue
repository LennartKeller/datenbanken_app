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
            <p class="card-header-title"  >
             {{collection.name}}
            </p>
          </header>
        </router-link>
      </div>
    </div>
    <br>
    <div class="columns is-mobile">
      <div class="column is-half is-offset-one-quarter">
        <div class="box">
      <b-field class="file">
        <b-upload v-model="file" expanded>
          <a class="button is-primary is-fullwidth">
            <b-icon icon="upload"></b-icon>
            <span>{{ file.name || "Click to upload"}}</span>
          </a>
        </b-upload>
      </b-field>
      <b-field>
        <b-upload v-model="dropFiles" multiple drag-drop expanded>
          <section class="section">
            <div class="content has-text-centered">
              <p>
                <b-icon icon="upload" size="is-large"></b-icon>
              </p>
              <p>Drop your files here or click to upload</p>
            </div>
          </section>
        </b-upload>
      </b-field>
      <div class="tags">
        <span v-for="(file, index) in dropFiles" :key="index" class="tag is-primary">
          {{file.name}}
          <button class="delete is-small" type="button" @click="deleteDropFile(index)"></button>
        </span>
      </div>
    </div>
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
      error: null,
      file: {},
      dropFiles: []
    }
  },
  methods: {
    getCollectionList () {
      $backend.fetchCollectionList()
        .then(response => { this.collectionList = response })
        .catch(error => { this.error.messagge = error })
    },
    deleteDropFile (index) {
      this.dropFiles.splice(index, 1)
    }
  },
  beforeMount () {
    this.getCollectionList()
  }
}
</script>

<style scoped>

</style>
