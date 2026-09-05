import { FastifyPluginAsync } from 'fastify'

const authRoutes: FastifyPluginAsync = async (fastify, opts) => {
  fastify.post('/verify', async (request, reply) => {
    // Backend endpoint to verify ID token and return user info
    try {
      const auth = request.headers['authorization'] as string | undefined
      if (!auth || !auth.startsWith('Bearer ')) return reply.code(401).send({ error: 'missing' })
      // Verification handled by middleware in protected routes; here we just echo placeholder
      return { ok: true }
    } catch (err) {
      return reply.code(500).send({ error: 'verification failed' })
    }
  })
}

export default authRoutes
