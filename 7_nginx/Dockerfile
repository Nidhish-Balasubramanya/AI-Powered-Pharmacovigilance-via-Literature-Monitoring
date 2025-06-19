FROM nginx:alpine

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy SSL certificates
COPY certs/ /etc/nginx/certs/

# Expose both HTTPS and HTTP (if using internal testing or ALB redirects)
EXPOSE 443
EXPOSE 80

# Run nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
