#!/usr/bin/env python3

import responder
from selenium import webdriver
import selenium
import time
import sys
import os
import re

api = responder.API()

# total arguments
# We need 2 arguments - the website URL (argv[1]) and the ICAO (argv[2])
#if len(sys.argv) != 3:
#    sys.exit('Expected use: snap.py <tar1090 base url> <icao>')

BASE_URL = os.environ.get('BASE_URL', 'https://globe.adsbexchange.com/')
LOAD_SLEEP_TIME = int(os.environ.get('LOAD_SLEEP_TIME', 1))
MAP_ARGS = os.environ.get('MAP_ARGS', 'zoom=11&hideSidebar&hideButtons&mapDim=0')

@api.route('/snap/{icao}')
async def snap_api(req, resp, *, icao):
  img = get_screenshot(icao)
  resp.content = img


def one_by_one_pixel():
  #return base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')
  return b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'


def get_screenshot(icao):
  '''Returns PNG as a binary. Doesn't serve arbitrary URLs because it'd be a security hole.'''
  icao = icao.upper()
  if len(icao) != 6 or not re.match('^[A-F\d]*$', icao):
    print(f"bad ICAO: {icao}")
    return one_by_one_pixel()
  #url = f"https://globe.adsbexchange.com/?icao={icao}"
  #url = f'https://globe.adsbexchange.com/?icao={icao}&zoom=11&hideSidebar&hideButtons'
  url = f'{BASE_URL}?icao={icao}&{MAP_ARGS}'
  print(f"pulling url: {url}")

  zoom = 75

  co = selenium.webdriver.chrome.options.Options()
  #co.add_argument("--delay 5")
  co.add_argument("--headless")
  co.add_argument("--no-sandbox")
  co.add_argument("--incognito")
  co.add_argument(f'window-size=1200x1600')
  browser = selenium.webdriver.Chrome(options=co)

  browser.get(url)
  elems = browser.find_elements_by_css_selector("#map_canvas canvas")
  if not len(elems):
    raise Exception("no elements found (eg missing map canvas)")
  elif not elems[0].is_displayed():
    raise Exception(f"have {len(elems)}, but the first isn't displayed")

  #browser.execute_script(f"document.body.style.zoom='{zoom}%'")

  # this sleep ensures the map is loaded. If everything but the map is loaded, increase the sleep.
  time.sleep(LOAD_SLEEP_TIME)
  return browser.get_screenshot_as_png()
  #return browser.save_screenshot(fname)
  # print(f"done {br}")

  #browser.quit()

  #return fname

if __name__ == '__main__':
  api.run(address='0.0.0.0')
