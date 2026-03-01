FROM node:22-alpine AS builder

WORKDIR /app

# Copy frontend package files
COPY frontend/package*.json ./
RUN npm install

# Copy frontend source
COPY frontend/ .

# Build production bundle
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# Serve with nginx
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html

# nginx config to handle React Router (SPA)
RUN printf 'server {\n  listen 80;\n  root /usr/share/nginx/html;\n  index index.html;\n  location / { try_files $uri $uri/ /index.html; }\n}\n' > /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
