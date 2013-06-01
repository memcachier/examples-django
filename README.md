# MemCachier Django Example

This is an example Django app that uses MemCachier to cache algebraic
computations in Heroku. This example is written with Django 1.4.

You can view a working version of this app
[here](http://memcachier-examples-django.herokuapp.com).
Running this app on your local machine in development will work as
well, although then you won't be using MemCachier -- you'll be using a
local dummy cache. MemCachier is currently only available in Heroku.

Setting up MemCachier to work in Django is very easy. You need to
make changes to requirements.txt, settings.py, and any app code that
you want cached. These changes are covered in detail below:

## requirements.txt

MemCachier has been tested with the pylibmc memcache client, but the
default client doesn't support SASL authentication. Run the following
commands to install the necessary pips:

~~~~ .shell
sudo port install libmemcached
LIBMEMCACHED=/opt/local pip install pylibmc
pip install django-pylibmc-sasl
~~~~

Don't forget to update your requirements.txt file with these new pips.
requirements.txt should have the following two lines:

~~~~
pylibmc==1.2.2
django-pylibmc-sasl==0.2.4
~~~~

## settings.py

Configure Django to use pylibmc with SASL authentication. You'll also
need to setup your environment, because pylibmc expects different
environment variables than MemCachier provides. Somewhere in your
settings.py file you should have the following lines:

~~~~ .python
os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '')
os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': os.environ.get('MEMCACHIER_SERVERS', ''),
        'TIMEOUT': 500,
        'BINARY': True,
    }
}
~~~~

Feel free to change the TIMEOUT setting to match your needs. You can
also leave this blank to accept the default value.

## Application Code

In your application, use django.core.cache methods to access
MemCachier. A description of the low-level caching API can be found
[here](https://docs.djangoproject.com/en/1.4/topics/cache/#the-low-level-cache-api).
All the built-in Django caching tools will work, too.

Take a look at `memcachier_algebra/views.py` in this repository for an
example.

## Get involved!

We are happy to receive bug reports, fixes, documentation enhancements,
and other improvements.

Please report bugs via the
[github issue tracker](http://github.com/memcachier/examples-django/issues).

Master [git repository](http://github.com/memcachier/examples-django):

* `git clone git://github.com/memcachier/examples-django.git`

## Licensing

This library is BSD-licensed.

