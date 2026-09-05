import { FastifyPluginAsync } from 'fastify'
import { verifyFirebaseToken } from '../middleware/auth'
import { Storage } from '@google-cloud/storage'

const storage = new Storage()
const bucketName = process.env.GCS_BUCKET_NAME

const routes: FastifyPluginAsync = async (fastify, opts) => {
  fastify.addHook('preHandler', verifyFirebaseToken as any)

  fastify.post('/:patientId/upload', async (request: any, reply) => {
    const parts = request.files()
    const uploaded: any[] = []
    for await (const part of parts) {
      if (part.file) {
        const filename = `${Date.now()}_${part.filename}`
        const bucket = storage.bucket(bucketName!)
        const file = bucket.file(`patients/${request.params.patientId}/reports/${filename}`)
        await new Promise((res, rej) => {
          const stream = file.createWriteStream({ resumable: false })
          part.file.pipe(stream)
          part.file.on('end', res)
          part.file.on('error', rej)
        })
        uploaded.push({ filename, path: `gs://${bucketName}/${file.name}` })
      }
    }
    return { uploaded }
  })
}

export default routes
