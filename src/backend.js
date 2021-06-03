import axios from 'axios'

let $axios = axios.create({
  baseURL: '/api/',
  timeout: 5000,
  headers: {'Content-Type': 'application/json'}
})

// Request Interceptor
$axios.interceptors.request.use(function (config) {
  config.headers['Authorization'] = 'Fake Token'
  return config
})

// Response Interceptor to handle and log errors
$axios.interceptors.response.use(function (response) {
  return response
}, function (error) {
  // Handle Error
  console.log(error)
  return Promise.reject(error)
})

export default {

  fetchResource () {
    return $axios.get(`resource/xxx`)
      .then(response => response.data)
  },

  fetchSecureResource () {
    return $axios.get(`secure-resource/zzz`)
      .then(response => response.data)
  },

  fetchTestResource () {
    return $axios.get('test/uuu')
      .then(response => response.data)
  },
  fetchText (textId) {
    return $axios.get('text/' + textId.toString())
      .then(response => response.data)
  },
  fetchCollectionList () {
    return $axios.get('collection')
      .then(response => response.data)
  },
  fetchTasksOfCollection (collectionId) {
    return $axios.get('collection/' + collectionId.toString() + '/tasks')
      .then(response => response.data)
  },
  fetchSequenceClassificationTaskConfig (taskId) {
    return $axios.get('sequence-classification/' + taskId.toString())
      .then(response => response.data)
  },
  postSequenceClassificationAnnotation (annotation, textId, taskId) {
    let url = '/text/' + textId.toString() + '/seq-class-task/' + taskId.toString() + '/annotation'
    return $axios.post(url, annotation)
      .then(response => response.data)
  },
  discardText (textId) {
    return $axios.get('text/' + textId.toString() + '/discard')
      .then(response => response.data)
  },
  fetchNextTextIds (collectionId) {
    return $axios.get('collection/' + collectionId.toString() + '/next')
      .then(response => response.data)
  },
  postCollectionFileUpload (fileObject) {
    return $axios.post('collection/add', fileObject)
      .then(response => response.data)
  }

}
