# ============================================
# DOCKERFILE - FRONTEND REACT
# Sistema de Zeladoria Urbana - Belém/PA
# ============================================

# ESTÁGIO 1: Build do React
FROM node:20-alpine AS builder

WORKDIR /app

# Copiar dependências primeiro (cache de layer)
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --silent

# Copiar código fonte
COPY frontend/ .

# Build de produção (variável injetada em build time)
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# ESTÁGIO 2: Servir com Nginx
FROM nginx:alpine

# Copiar arquivos buildados
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar config do nginx para SPA (react-router-dom)
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
