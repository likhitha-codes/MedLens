import fastify from 'fastify'
import helmet from 'fastify-helmet'
import multipart from 'fastify-multipart'
import rateLimit from 'fastify-rate-limit'
import pino from 'pino'
import authRoutes from './routes/auth'
import patientRoutes from './routes/patients'
import reportRoutes from './routes/reports'

const logger = pino({ level: process.env.LOG_LEVEL || 'info' })
const app = fastify({ logger })

app.register(helmet)
app.register(multipart)
app.register(rateLimit, { max: 1000 })

app.register(authRoutes, { prefix: '/api/auth' })
app.register(patientRoutes, { prefix: '/api/patients' })
app.register(reportRoutes, { prefix: '/api/reports' })

app.get('/health', async (req, reply) => ({ status: 'healthy' }))

const port = Number(process.env.PORT || 8080)
app.listen({ port, host: '0.0.0.0' }).then(() => logger.info(`Server listening on ${port}`))
