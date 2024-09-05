# debian:unstable-20240211-slim
FROM debian@sha256:2fc255e56e2fee2c7597883e3c835c330c3e71d9144675790a9f84eb2548fd57

COPY website/requirements.txt /tmp/requirements.txt

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
  git \
  python3-pip \
  texlive-full \
  wget

RUN wget -q https://github.com/jgm/pandoc/releases/download/3.1.12.1/pandoc-3.1.12.1-1-amd64.deb && \
  dpkg -i pandoc-3.1.12.1-1-amd64.deb

# taken from pandoc/dockerfiles
ARG TEMPLATES_DIR=/.pandoc/templates
RUN mkdir -p ${TEMPLATES_DIR} && \
    ln -s /.pandoc /root/.pandoc

RUN pip3 install -r /tmp/requirements.txt --no-cache-dir --break-system-packages && \
  rm -f /tmp/requirements.txt

# make cache writeable for docker user/lualatex
RUN chmod a+rw /var/lib/texmf

WORKDIR /data

