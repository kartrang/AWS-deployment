import time, urllib.request, sys

# Give server a moment to start
time.sleep(2)

try:
    r = urllib.request.urlopen('http://127.0.0.1:5000', timeout=6)
    print('HTTP', r.getcode())
except Exception as e:
    print('REQUEST_ERROR', repr(e))
    sys.exit(1)
