import os
import pylibmc
import sys
import time

mc_srvs = os.environ.get('MEMCACHIER_SERVERS', '').split(',')
mc_user = os.environ.get('MEMCACHIER_USERNAME', '')
mc_pass = os.environ.get('MEMCACHIER_PASSWORD', '')

mc = pylibmc.Client(
        mc_srvs,
        username=mc_user,
        password=mc_pass,
        binary=True,
        behaviors={
            # Enable faster IO
            'tcp_nodelay': True,
            'tcp_keepalive': True,

            # Timeout settings
            'connect_timeout': 2000, # ms
            'send_timeout': 750 * 1000, # us
            'receive_timeout': 750 * 1000, # us
            '_poll_timeout': 2000, # ms

            # Better failover
            'ketama': True,
            'remove_failed': 1,
            'retry_timeout': 2,
            'dead_timeout': 30,
        }
    )

print mc.behaviors

mc["get_key"] = "value"

while True:
    try:
        time.sleep(0.5)
        print mc["get_key"]
    except KeyboardInterrupt:
        print "Exit..."
        break
    except:
        print "Unexpected error:", sys.exc_info()[0]

