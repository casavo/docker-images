FROM alpine:3 as fetcher

ARG ABS=2.6.0
ARG DOCKER_BUILDX=v0.8.2
ARG DOCKER_COMPOSE=v2.5.0
ARG YQ=v4.25.1

RUN apk add --no-cache curl

WORKDIR /wrk

RUN mkdir -p bin
RUN curl -sSL https://github.com/abs-lang/abs/releases/download/${ABS}/abs-linux-amd64 > bin/abs \
    && chmod +x bin/abs
RUN curl -sSL https://github.com/docker/buildx/releases/download/${DOCKER_BUILDX}/buildx-${DOCKER_BUILDX}.linux-amd64 > docker-buildx \
    && chmod +x docker-buildx
RUN curl -sSL https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE}/docker-compose-linux-x86_64 > docker-compose \
    && chmod +x docker-compose
RUN curl -sSL https://github.com/mikefarah/yq/releases/download/${YQ}/yq_linux_amd64 > bin/yq \
    && chmod +x bin/yq

FROM ghcr.io/actions-runner-controller/actions-runner-controller/actions-runner-dind:v2.294.0-ubuntu-20.04

COPY --from=fetcher /wrk/docker-buildx /usr/libexec/docker/cli-plugins/docker-buildx
COPY --from=fetcher /wrk/docker-compose /usr/libexec/docker/cli-plugins/docker-compose
COPY --from=fetcher /wrk/bin/* /usr/local/bin/

RUN sudo mv /usr/bin/entrypoint.sh /usr/bin/entrypoint_runner.sh \
    && sudo mkdir -p /etc/bootstrap_scripts

COPY bootstrap.abs entrypoint.sh /usr/bin/

RUN curl -fsSL https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip > /tmp/awscli.zip \
    && unzip /tmp/awscli.zip -d /tmp \
    && sudo ./tmp/aws/install \
    && rm -rf /tmp/aws*

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash - \
    && sudo apt-get install -y nodejs \
    && sudo npm install -g yarn \
    && sudo rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - \
    && echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list

RUN sudo apt-get update -y \
    && sudo apt-get install -y --no-install-recommends \
        libasound2 \
        libgbm-dev \
        libgconf-2-4 \
        libgtk-3-0 \
        libnss3 \
        libxss1 \
        postgresql-client \
        xvfb \
        google-chrome-stable \
    && sudo rm -rf /var/lib/apt/lists/*

ENV LANG=C.UTF-8
