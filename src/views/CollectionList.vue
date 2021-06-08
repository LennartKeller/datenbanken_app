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
      <div class="box collection-card" v-for="collection in collectionList" :key="collection.id">
          <div class="hero">
            <div class="hero-body">
              <router-link
                  :to="{name: 'annotation-view', params: {collectionId: collection.id}}"
                  title="Open Collection">
                  <div class="subtitle">
                    <p>{{collection.name}}</p>
                    <div class="container progress-bar-container">
                    <CollectionProgressBar :collection-id="collection.id" :key="collection.id"></CollectionProgressBar>
                    </div>
                  </div>
              </router-link>
              <br>
               <a :href="'/api/collection/' + collection.id.toString() + '/download'">
                <span class="download-button" title="Download Collection.">
                  <b-icon
                      pack="fas"
                      icon="download"
                      size="is-medium"/>
                  <!--<div>Download Collection.</div>-->
                </span>
               </a>
            </div>
          </div>
      </div>
    </div>
    <br>
    <div class="columns is-mobile">
      <div class="column is-half is-offset-one-quarter">
        <div class="box">
          <section class="hero">
            <div class="hero-body">
              <p class="title">
                Add
              </p>
              <p class="subtitle">
                Upload new collections.
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
              <p>Drop your collection-configurations here.</p>
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
import CollectionProgressBar from './CollectionProgressBar'
export default {
  name: 'CollectionList',
  components: {CollectionProgressBar},
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
  .collection-card {margin: 0.5em;}
  .download-button {margin-right: 1em;}
  .progress-bar-container{margin-top: 0.5em;}
</style>
