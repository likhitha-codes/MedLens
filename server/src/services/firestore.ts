import { Firestore } from '@google-cloud/firestore'

const projectId = process.env.GOOGLE_CLOUD_PROJECT
const firestore = new Firestore({ projectId })

export default firestore
