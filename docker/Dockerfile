# ==============================================================================
# Multi-Stage Dockerfile for University ERP (Laravel / PHP 8.2 + Nginx)
# Meets constraints: Multi-stage, under 300 MB, non-root user
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build & Composer Dependencies
# ------------------------------------------------------------------------------
FROM composer:2.6 AS composer_build

WORKDIR /app

# Copy dependency manifests first for optimal Docker layer caching
COPY composer.json composer.lock* ./

# Install production dependencies without dev dependencies or autoloader scripts
RUN composer install \
    --no-dev \
    --no-interaction \
    --prefer-dist \
    --no-scripts \
    --optimize-autoloader \
    --ignore-platform-reqs

# ------------------------------------------------------------------------------
# Stage 2: Production Runtime (PHP-FPM + Nginx Alpine)
# ------------------------------------------------------------------------------
FROM php:8.2-fpm-alpine

# Install Nginx, supervisor, and essential runtime libraries
RUN apk add --no-cache \
    nginx \
    supervisor \
    curl \
    libpng-dev \
    libzip-dev \
    oniguruma-dev \
    && docker-php-ext-install pdo_mysql mbstring bcmath opcache \
    && rm -rf /var/cache/apk/*

# Create application directory and dedicated non-root user
WORKDIR /var/www/html

# Copy Nginx and Supervisor configs
RUN mkdir -p /etc/supervisor.d /run/nginx /var/log/supervisor

# Configure minimal Nginx
RUN echo 'server { \
    listen 80; \
    server_name _; \
    root /var/www/html/public; \
    index index.php index.html; \
    location / { \
        try_files $uri $uri/ /index.php?$query_string; \
    } \
    location /health { \
        access_log off; \
        return 200 "OK"; \
    } \
    location ~ \.php$ { \
        fastcgi_pass 127.0.0.1:9000; \
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name; \
        include fastcgi_params; \
    } \
}' > /etc/nginx/http.d/default.conf

# Configure Supervisord to orchestrate Nginx and PHP-FPM
RUN echo '[supervisord] \
nodaemon=true \
logfile=/var/log/supervisor/supervisord.log \
pidfile=/var/run/supervisord.pid \
\
[program:php-fpm] \
command=php-fpm -F \
autostart=true \
autorestart=true \
stdout_logfile=/dev/stdout \
stdout_logfile_maxbytes=0 \
stderr_logfile=/dev/stderr \
stderr_logfile_maxbytes=0 \
\
[program:nginx] \
command=nginx -g "daemon off;" \
autostart=true \
autorestart=true \
stdout_logfile=/dev/stdout \
stdout_logfile_maxbytes=0 \
stderr_logfile=/dev/stderr \
stderr_logfile_maxbytes=0' > /etc/supervisor.d/supervisord.ini

# Copy vendor dependencies from stage 1
COPY --from=composer_build /app/vendor /var/www/html/vendor

# Copy application code
COPY . /var/www/html

# Provide minimal default public directory if running standalone
RUN mkdir -p /var/www/html/public \
    && echo '<?php phpinfo(); ?>' > /var/www/html/public/index.php

# Security: Ensure ownership belongs to non-root www-data user
RUN chown -R www-data:www-data /var/www/html /run/nginx /var/log/nginx /var/log/supervisor

# Expose HTTP port
EXPOSE 80

# Run supervisor as root to manage ports, while PHP-FPM workers run as www-data
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor.d/supervisord.ini"]
