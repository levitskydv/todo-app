#Old version template
#FROM nginx:alpine
#COPY index.html /usr/share/nginx/html/
#EXPOSE 30080
#CMD ["nginx", "-g", "daemon off;"]

FROM php:8.2-apache

COPY index.html /var/www/html/

EXPOSE 30080

CMD ["apache2-foreground"]