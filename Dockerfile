FROM ghcr.io/fredclausen/docker-baseimage:python

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive


RUN set -x && \
TEMP_PACKAGES=() && \
KEPT_PACKAGES=() && \
KEPT_PACKAGES+=(python3-selenium) && \
KEPT_PACKAGES+=(chromium) && \
KEPT_PACKAGES+=(chromium-driver) && \
#
# Install all these packages:
    apt-get update -q && \
    apt-get install -q -o APT::Autoremove::RecommendsImportant=0 -o APT::Autoremove::SuggestsImportant=0 -o Dpkg::Options::="--force-confold" --force-yes -y --no-install-recommends  --no-install-suggests\
        ${KEPT_PACKAGES[@]} \
        ${TEMP_PACKAGES[@]} && \
#
# Clean up:
    apt-get remove -q -y ${TEMP_PACKAGES[@]} && \
    apt-get autoremove -q -o APT::Autoremove::RecommendsImportant=0 -o APT::Autoremove::SuggestsImportant=0 -y && \
    apt-get clean -q -y && \
    rm -rf /src/* /tmp/* /var/lib/apt/lists/*


COPY requirements.txt /opt/app/
RUN pip3 install -r /opt/app/requirements.txt

COPY *.py /opt/app/

WORKDIR /opt/app/
CMD /opt/app/snapapi.py
EXPOSE 5042
