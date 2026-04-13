# ============================================
# DOCKERFILE - FRONTEND ESTÁTICO (HTML/JS/CSS)
# Sistema de Zeladoria Urbana - Belém/PA
# ============================================

FROM nginx:alpine

# Instalar gettext para envsubst (substituição de $PORT)
RUN apk add --no-cache gettext

# Copiar arquivo HTML principal e manifest
COPY index.html /usr/share/nginx/html/index.html
COPY manifest.json /usr/share/nginx/html/manifest.json

# Copiar config do nginx como template
COPY nginx.conf /etc/nginx/conf.d/default.conf.template

# Script de inicialização
CMD ["/bin/sh", "-c", "envsubst '$PORT' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
