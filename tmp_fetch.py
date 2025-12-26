import urllib.request
r = urllib.request.urlopen('http://127.0.0.1:5000')
data = r.read(1000)
print(data.decode('utf-8', errors='replace'))
print('\nHTTP CODE:', r.getcode())
