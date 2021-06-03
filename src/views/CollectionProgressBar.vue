<template>
<div class="collection-progress">
  <b-progress
      size="is-large"
      :value="annotated"
      :max="unannotated"
      :show-value="true"
      format="percent"
      :precision="1"
      :type="format"
      :indeterminate="this.annotated === null"
  />
</div>
</template>

<script>
import $backend from '@/backend'
export default {
  name: 'CollectionProgressBar',
  props: ['collectionId'],
  data () {
    return {
      'annotated': null,
      'unannotated': null
    }
  },
  methods: {
    getCollectionProgress () {
      $backend.getCollectionProgress(this.collectionId).then(response => {
        this.annotated = response.annotated
        this.unannotated = response.unannotated
      })
    }
  },
  computed: {
    format: function () {
      if (this.annotated === this.unannotated) {
        return 'is-success'
      } else {
        return 'is-info'
      }
    }
  },
  beforeMount () {
    this.getCollectionProgress()
  }
}
</script>

<style scoped>
.collection-progress {margin-left: 3em;}
</style>
