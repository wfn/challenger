import requests
import json
import time

SLEEP_TIME = 0.25
SLEEP_THRESHOLD = 100

class OnionooError(Exception):
  pass

def query(resource, params):
  if not resource in ['summary', 'details', 'bandwidth', 'weights',
                      'clients', 'uptime']:
    raise OnionooError('Invalid query (Unknown document)')

  url = 'https://onionoo.torproject.org/%s' % (resource,)

  r = requests.get(url, params=params)
  if r.status_code == 200:
    return r.json()
  else:
    raise OnionooError('Onionoo replied with error: %s (%s)' % (
                       r.status_code, r.reason))

def download_documents(resource_name, fingerprints):
  downloads = []
  do_sleep = (len(fingerprints) > SLEEP_THRESHOLD)
  for fingerprint in fingerprints:
    doc = query(resource_name, {'lookup':fingerprint})
    downloads.append(doc)
    if do_sleep: # if there are lots of fingerprints to look up, it's a good
                 # idea to not rush, and to have Onionoo take a breath.
      time.sleep(SLEEP_TIME)
  return downloads
