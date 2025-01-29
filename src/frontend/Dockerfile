# frontend/Dockerfile
FROM nginx:alpine
RUN rm /usr/share/nginx/html/*
COPY bootstrap/v1/ /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]