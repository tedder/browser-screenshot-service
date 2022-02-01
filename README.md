# browser-screenshot-service
web browser screenshot as a service! Designed for the [mikenye ADSB decoding](https://mikenye.gitbook.io/ads-b/) world.

# execution example

    docker run -p 5042:5042 \
      -e MAP_ARGS='zoom=11&hideSidebar&hideButtons&mapDim=0.3' \
      -e BASE_URL='https://ramonk.net/tar1090/' -it tedder42/browser-screenshot-service:latest

    curl http://localhost:5042/snap/a9b67c

Fix the URL, make sure the ICAO actually exists, use upper or lower case. Some of the environment vars were listed to show what might be put in there.

There's a bit of sanity testing against the ICAO code in the URL. Enter something invalid and it'll return a 1x1 pixel.

These are the environment variables that are supported:
| Variable | Values | Description |
|---|---|---|
| BASE_URL | The base URL of your `tar1090` instance. Default: https://globe.adsbexchange.com/ | This determines the base URL of the location where the `screenshot` container will browse to get the image |
| LOAD_SLEEP_TIME | Positive integer values. Default = 1 | This parameter determines how many seconds the container will wait until the page is rendered before a screenshot is taken. Increase the value if the screenshots show incompletely rendered pages (--check the aircraft picture in the left top, as that one often gets loaded last! For Raspberry Pi 4, a good starting value should be between `10` and `15`. For Raspberry Pi 3B+, this value should be `15` - `20` or even larger. |
| MAP_ARGS |  Default: `zoom=11&hideSidebar&hideButtons&mapDim=0` Example/recommended value: `zoom=11.5&hideSidebar&hideButtons&mapDim=0.2&monochromeMarkers=ff0000&outlineColor=505050&iconScale=1.5&enableLabels&extendedLabels=2&trackLabels` | Arguments passed to the `tar1090` URL. |
| PAGE_ZOOM | Positive integer between `1` and `100`. Default: `100` | Browser page zoom |
| DISABLE_SHM | `true` / `false`. Default: `false` | Disable use of Shared Memory |
| DISABLE_VIZ | `true` / `false`. Default: `false` | Disable the internal browser's visual display |
| MAXTIME | Positive integer values. Default = 30 | Maximum time in seconds the container will wait to render a screenshot before giving up completely. If the container often shows time-out logs, increase this value. |
| CANVAS_SIZE | `width`x`height`. Default: 1200x1600 | Size (`width`x`height` in pixels) of the rendered screenshot |
