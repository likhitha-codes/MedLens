import { FastifyPluginAsync } from 'fastify'
import { verifyFirebaseToken } from '../middleware/auth'

const routes: FastifyPluginAsync = async (fastify, opts) => {
  fastify.addHook('preHandler', verifyFirebaseToken as any)

  fastify.get('/', async (request, reply) => {
    // List patients placeholder
    return { patients: [] }
  })

  fastify.post('/', async (request, reply) => {
    // Create patient placeholder
    const body = request.body as any
    return { id: 'patient_123', ...body }
  })

  fastify.get('/:id', async (request, reply) => {
    const { id } = request.params as any
    return { id, name: 'Demo Patient' }
  })
}

export default routes
