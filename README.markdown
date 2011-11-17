Adfly Proxies
=============

Behold, the proxies for adf.ly.

Supply one of these with the five trailing characters of an adfly link and it will redirect you to its destination.

PHP
---

Download `adflyproxy.php` and put it in your DocumentRoot somewhere. Simply supply the five trailing characters as the `code` GET variable.

Python/mod\_wsgi
---------------

This script requires apache because it uses some environmental variables apache sets.

Download `adflyproxy.wsgi` and put it somewhere outside your DocumentRoot. Then alias it in your `httpd.conf`. Skip the trailing slash on the first argument of the `WSGIScriptAlias`.

    WSGIScriptAlias /ad /home/you/wsgi_scripts/adflyproxy.wsgi

Django
------

### Easy method ###

Copy the `proxy` function from `views` and put it in your own app. Take a look at the `urls.py` file to see an example of its use.

### Fancy method ###

Run `./setup.py install` as usual to install the django app. 

Afterward, import the `proxy` view from `adflyproxy.views` and pass it the 5 trailing characters of the adfly link as the `code` parameter.

