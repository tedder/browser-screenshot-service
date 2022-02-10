#FROM ghcr.io/sdr-enthusiasts/docker-baseimage:python
FROM debian:stable-slim
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
EXPOSE 5042

RUN apt update && apt install -y python3-selenium chromium chromium-driver python3-pip vim
COPY requirements.txt /opt/app/
RUN pip3 install -r /opt/app/requirements.txt

COPY *.py /opt/app/

WORKDIR /opt/app/
CMD /opt/app/snapapi.py

#MAP_ARGS='zoom=11&hideSidebar&hideButtons&mapDim=0.3' BASE_URL='http://192.168.3.67:8078/' python3 snapapi.py
