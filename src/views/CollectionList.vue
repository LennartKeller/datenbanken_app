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
      <div class="card collection-card" v-for="collection in collectionList" :key="collection.id">
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
          <section class="hero">
            <div class="hero-body">
              <p class="title">
                Upload
              </p>
            </div>
          </section>
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
      <div class="upload-button-container">
        <b-button id="upload-button"
                  size="is-medium"
                  icon-left="upload"
                  v-if="dropFiles.length > 0"
                  v-on:click="uploadAllFiles">
          Upload
        </b-button>
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
    },
    uploadAllFiles () {
      while (this.dropFiles.length > 0) {
        let file = this.dropFiles.pop()
        let formData = new FormData()
        formData.append('file', file)
        this.uploadFile(formData)
      }
    },
    uploadFile (fileObject) {
      $backend.postCollectionFileUpload(fileObject)
        .then((response) => {
          this.$buefy.dialog.alert(response.message)
          this.getCollectionList()
        })
        .catch((error) => {
          this.error = error
        })
    }
  },
  beforeMount () {
    this.getCollectionList()
  }
}
</script>

<style scoped>
  .collection-card {padding: 0.5em;}
</style>
