import os
import pylibmc
import sys
import time

mc = pylibmc.Client(
        [os.environ['MEMCACHIER_SERVERS']],
        binary=True,
        username=os.environ['MEMCACHIER_USERNAME'],
        password=os.environ['MEMCACHIER_PASSWORD'],
        behaviors={
            'no_block': True,
            'tcp_nodelay': True,
            'tcp_keepalive': True,
            'remove_failed': 4,
            'retry_timeout': 2,
            # 'dead_timeout': 10,
            '_poll_timeout': 2000
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

