FROM node:22-alpine AS builder

WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .

ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# Production stage
FROM node:22-alpine
RUN npm install -g serve
WORKDIR /app
COPY --from=builder /app/dist ./dist

# Railway injects PORT env var — serve reads it natively
EXPOSE 8080
CMD serve -s dist -l ${PORT:-8080}
