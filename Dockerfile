FROM ghcr.io/sdr-enthusiasts/docker-baseimage:python
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
EXPOSE 5042

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

COPY requirements.txt /opt/app/

RUN set -x && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
      chromium \
      chromium-driver \
      gcc \
      python3-dev \
      python3-pip \
      python3-selenium \
      vim \
      && \
    python3 -m pip install --no-cache-dir -r /opt/app/requirements.txt && \
    # clean up
    apt-get autoremove -y && \
    rm -rf /src/* /tmp/* /var/lib/apt/lists/*

COPY *.py /opt/app/

WORKDIR /opt/app/
CMD [ "/opt/app/snapapi.py" ]

#MAP_ARGS='zoom=11&hideSidebar&hideButtons&mapDim=0.3' BASE_URL='http://192.168.3.67:8078/' python3 snapapi.py
