FROM node:20-alpine AS builder
WORKDIR /app

# Build client
COPY client/package.json client/package-lock.json* ./client/
WORKDIR /app/client
RUN npm ci || true
COPY client/ ./
RUN npm run build || true

# Build server
WORKDIR /app
COPY server/package.json server/package-lock.json* ./server/
WORKDIR /app/server
RUN npm ci || true
COPY server/ ./
RUN npm run build || true

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/server/dist ./server/dist
COPY --from=builder /app/client/dist ./client/dist
WORKDIR /app/server
ENV PORT=8080
EXPOSE 8080
CMD ["node","dist/server.js"]
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
ENV FLASK_ENV=production
EXPOSE 5000
CMD ["python", "app.py"]
