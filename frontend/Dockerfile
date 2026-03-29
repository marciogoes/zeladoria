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

# Instalar gettext para envsubst
RUN apk add --no-cache gettext

# Copiar arquivos buildados
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar config do nginx como template
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf.template

# Script de inicialização que substitui $PORT e inicia o nginx
CMD ["/bin/sh", "-c", "envsubst '$PORT' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
