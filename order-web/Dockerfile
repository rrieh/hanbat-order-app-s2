# Multi-architecture: linux/amd64, linux/arm64
FROM nginx:alpine

ARG APP_VERSION=1.0.0
ENV APP_VERSION=${APP_VERSION}

COPY index.html /usr/share/nginx/html/index.html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -qO- http://localhost/health || exit 1
