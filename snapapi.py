#!/usr/bin/env python3

import responder
import selenium.webdriver.support.expected_conditions as EC
import selenium
import time
import sys
import os
import re
import logging

logging.basicConfig(level=logging.CRITICAL, format='%(message)s')
log = logging.getLogger(__file__)
log.propagate = True
log.setLevel(logging.DEBUG) # notset, debug, info, warning, error, critical


api = responder.API()

BASE_URL = os.environ.get('BASE_URL', 'https://globe.adsbexchange.com/')
LOAD_SLEEP_TIME = int(os.environ.get('LOAD_SLEEP_TIME', 1))
MAP_ARGS = os.environ.get('MAP_ARGS', 'zoom=11&hideSidebar&hideButtons&mapDim=0')
PAGE_ZOOM = int(os.environ.get('PAGE_ZOOM', '100'))

@api.route('/snap/{icao}')
async def snap_api(req, resp, *, icao):
  img = get_screenshot(icao)
  resp.content = img

def safe_url(u):
  '''Just seeing if things are fully formed.'''
  u = re.sub(r'[\'"]', '', u)
  if not re.match('^http(s?)://', u):
    u = f"http://{u}"
  if not u.endswith('/'):
    u += '/'
  return u

def one_by_one_pixel():
  #return base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')
  return b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'


def get_screenshot(icao):
  '''Returns PNG as a binary. Doesn't serve arbitrary URLs because it'd be a security hole.'''

  start_t = time.time()
  icao = icao.upper()
  log.warning("hi.")

  if len(icao) != 6 or not re.match('^[A-F\d]*$', icao):
    log.error(f"bad ICAO: {icao}")
    return one_by_one_pixel()
  #url = f"https://globe.adsbexchange.com/?icao={icao}"
  #url = f'https://globe.adsbexchange.com/?icao={icao}&zoom=11&hideSidebar&hideButtons'
  _base = safe_url(BASE_URL)
  url = f'{_base}?icao={icao}&{MAP_ARGS}'
  log.info(f"pulling url: {url}")

  co = selenium.webdriver.chrome.options.Options()
  #co.add_argument("--delay 5")
  co.add_argument("--headless")
  co.add_argument("--no-sandbox")
  co.add_argument("--incognito")
  co.add_argument(f'window-size=1200x1600')
  browser = selenium.webdriver.Chrome(options=co)

  browser.get(url)

  # https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html
  # https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.wait.html
  # second argument to WebDriverWait = timeout in seconds
  #cond = EC.presence_of_all_elements_located( (selenium.webdriver.common.by.By.CSS_SELECTOR, "#map_canvas") )
  cond = EC.visibility_of_all_elements_located( (selenium.webdriver.common.by.By.CSS_SELECTOR, "#map_canvas") )
  elem0 = selenium.webdriver.support.wait.WebDriverWait(browser, 20).until(cond)

  if PAGE_ZOOM and PAGE_ZOOM != 100:
    log.debug(f"zooming: {PAGE_ZOOM}")
    browser.execute_script(f"document.body.style.zoom='{PAGE_ZOOM}%'")

  # this sleep ensures the map is loaded. If everything but the map is loaded, increase the sleep.
  # Even with the "conditions" above, having zero sleep tends to show poorly rendered map tiles.
  time.sleep(LOAD_SLEEP_TIME)
  ss = browser.get_screenshot_as_png()

  delta_t = time.time() - start_t
  log.debug(f"elapsed time: {delta_t:.2f}sec")

  return ss

if __name__ == '__main__':
  api.run(address='0.0.0.0')
