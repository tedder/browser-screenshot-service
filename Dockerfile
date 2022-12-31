FROM ghcr.io/sdr-enthusiasts/docker-baseimage:python

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

COPY requirements.txt /opt/app/

RUN set -x && \
TEMP_PACKAGES=() && \
KEPT_PACKAGES=() && \
KEPT_PACKAGES+=(python3-selenium) && \
KEPT_PACKAGES+=(chromium) && \
KEPT_PACKAGES+=(chromium-driver) && \
KEPT_PACKAGES+=(python3-uvloop) && \
TEMP_PACKAGES+=(gcc) &&\
TEMP_PACKAGES+=(python3-dev) && \
TEMP_PACKAGES+=(python3-distutils-extra) && \
#
# Install all these packages:
    apt-get update -q && \
    apt-get install -q -o APT::Autoremove::RecommendsImportant=0 -o APT::Autoremove::SuggestsImportant=0 -o Dpkg::Options::="--force-confold" --force-yes -y --no-install-recommends  --no-install-suggests\
        ${KEPT_PACKAGES[@]} \
        ${TEMP_PACKAGES[@]} && \
#
    pip install -U setuptools && \
    pip3 install -r /opt/app/requirements.txt && \
    pip install --upgrade typesystem==0.2.5 && \
#
# Clean up:
    apt-get remove -q -y ${TEMP_PACKAGES[@]} && \
    apt-get autoremove -q -o APT::Autoremove::RecommendsImportant=0 -o APT::Autoremove::SuggestsImportant=0 -y && \
    apt-get clean -q -y && \
    rm -rf /src/* /tmp/* /var/lib/apt/lists/*


COPY *.py /opt/app/

WORKDIR /opt/app/
CMD /opt/app/snapapi.py
EXPOSE 5042
