import { FastifyReply, FastifyRequest } from 'fastify'
import admin from 'firebase-admin'

if (!admin.apps.length) {
  const projectId = process.env.FIREBASE_PROJECT_ID
  const clientEmail = process.env.FIREBASE_CLIENT_EMAIL
  const privateKey = process.env.FIREBASE_PRIVATE_KEY?.replace(/\\n/g, '\n')
  admin.initializeApp({
    credential: admin.credential.cert({ projectId, clientEmail, privateKey }),
  })
}

export async function verifyFirebaseToken(request: FastifyRequest, reply: FastifyReply) {
  try {
    const auth = request.headers['authorization'] as string | undefined
    if (!auth || !auth.startsWith('Bearer ')) {
      reply.code(401).send({ error: 'Missing or invalid authorization header' })
      return
    }
    const idToken = auth.split(' ', 2)[1]
    const decoded = await admin.auth().verifyIdToken(idToken)
    // attach user info
    ;(request as any).user = { uid: decoded.uid, email: decoded.email, role: decoded.role || 'user' }
  } catch (err) {
    reply.code(401).send({ error: 'Unauthorized' })
  }
}
