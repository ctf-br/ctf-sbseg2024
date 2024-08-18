FROM php:8.2.12-cli-alpine

COPY --from=composer:latest /usr/bin/composer /usr/local/bin/composer

WORKDIR /app

COPY ./index.php ./
COPY ./templates ./templates
COPY ./classes ./classes

COPY ./flag.txt /flag.txt
RUN mv /flag.txt /flag.txt

RUN composer require smarty/smarty

COPY ./openbdir.ini /usr/local/etc/php/conf.d/openbdir.ini

ENTRYPOINT ["php", "-S", "0.0.0.0:1337", "index.php"]