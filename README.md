# MemCachier Django Example App

This is an example Django app that uses
[MemCachier](http://www.memcachier.com) to cache algebraic
computations. This example is written with Django 1.6.5.

You can view a working version of this app
[here](http://memcachier-examples-django.herokuapp.com) that uses
[MemCachier on Heroku](https://addons.heroku.com/memcachier).
Running this app on your local machine in development will work as
well, although then you won't be using MemCachier -- you'll be using a
local dummy cache. MemCachier is currently only available with various
cloud providers.

Setting up MemCachier to work in Django is very easy. You need to
make changes to requirements.txt, settings.py, and any app code that
you want cached. These changes are covered in detail below.

## Deploy to Heroku

You can deploy this app yourself to Heroku to play with.

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Building

It is best to use the python `virtualenv` tool to build locally:

~~~~ .sh
$ virtualenv -p python2 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ DEVELOPMENT=1 python manage.py runserver
~~~~

Then visit `http://localhost:8000` to view the app. Alternatively you
can use foreman and gunicorn to run the server locally (after copying
`dev.env` to `.env`):

~~~~ .sh
$ foreman start
~~~~

## Deploy to Heroku

Run the following commands to deploy the app to Heroku:

~~~~ .sh
$ git clone https://github.com/memcachier/examples-django.git
$ cd examples-django
$ heroku create
$ heroku addons:add memcachier:dev
$ git push heroku master:master
$ heroku open
~~~~

## requirements.txt

MemCachier has been tested with the pylibmc memcache client, but the
default client doesn't support SASL authentication. Run the following
commands to install the necessary pips:

~~~~ .shell
sudo brew install libmemcached
pip install django-pylibmc pylibmc
~~~~

Don't forget to update your requirements.txt file with these new pips.
requirements.txt should have the following two lines:

~~~~
django-pylibmc==0.6.0
pylibmc==1.5.0
~~~~

## Configuring MemCachier (settings.py)

To configure Django to use pylibmc with SASL authentication. You'll also need
to setup your environment, because pylibmc expects different environment
variables than MemCachier provides. Somewhere in your `settings.py` file you
should have the following lines:

~~~~ .python
os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

CACHES = {
    'default': {
        # Use pylibmc
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',

        # Use binary memcache protocol (needed for authentication)
        'BINARY': True,

        # TIMEOUT is not the connection timeout! It's the default expiration
        # timeout that should be applied to keys! Setting it to `None`
        # disables expiration.
        'TIMEOUT': None,
        'OPTIONS': {
            # Enable faster IO
            'no_block': True,
            'tcp_nodelay': True,

            # Keep connection alive
            'tcp_keepalive': True,

            # Timeout for set/get requests (sadly timeouts don't mark a
            # server as failed, so failover only works when the connection
            # is refused)
            '_poll_timeout': 2000,

            # Use consistent hashing for failover
            'ketama': True,

            # Configure failover timings
            'connect_timeout': 2000,
            'remove_failed': 4,
            'retry_timeout': 2,
            'dead_timeout': 10
        }
    }
}
~~~~

Feel free to change the `_poll_timeout` setting to match your needs.

## Persistent Connections

By default, Django doesn't use persistent connections with memcached. This is a
huge performance problem, especially when using SASL authentication as the
connection setup is even more expensive than normal.

You can fix this by putting the following code in your `wsgi.py` file:

~~~~ .python
# Fix django closing connection to MemCachier after every request (#11331)
from django.core.cache.backends.memcached import BaseMemcachedCache
BaseMemcachedCache.close = lambda self, **kwargs: None

~~~~

There is a bug file against Django for this issue
([#11331](https://code.djangoproject.com/ticket/11331)).

## Application Code

In your application, use django.core.cache methods to access
MemCachier. A description of the low-level caching API can be found
[here](https://docs.djangoproject.com/en/1.4/topics/cache/#the-low-level-cache-api).
All the built-in Django caching tools will work, too.

Take a look at
[memcachier_algebra/views.py](https://github.com/memcachier/examples-django/blob/master/memcachier_algebra/views.py)
in this repository for an example.

## Get involved!

We are happy to receive bug reports, fixes, documentation enhancements,
and other improvements.

Please report bugs via the
[github issue tracker](http://github.com/memcachier/examples-django/issues).

Master [git repository](http://github.com/memcachier/examples-django):

* `git clone git://github.com/memcachier/examples-django.git`

## Licensing

This library is BSD-licensed.

