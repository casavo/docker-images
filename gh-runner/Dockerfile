FROM alpine:3 as fetcher

ARG DOCKER_BUILDX=v0.8.2
ARG DOCKER_COMPOSE=v2.5.0
ARG YQ=v4.25.1

RUN apk add --no-cache curl

WORKDIR /wrk

RUN mkdir -p bin
RUN curl -sSL https://github.com/docker/buildx/releases/download/${DOCKER_BUILDX}/buildx-${DOCKER_BUILDX}.linux-amd64 > docker-buildx \
    && chmod +x docker-buildx
RUN curl -sSL https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE}/docker-compose-linux-x86_64 > docker-compose \
    && chmod +x docker-compose
RUN curl -sSL https://github.com/mikefarah/yq/releases/download/${YQ}/yq_linux_amd64 > bin/yq \
    && chmod +x bin/yq

FROM summerwind/actions-runner:latest

COPY --from=fetcher /wrk/docker-buildx /usr/libexec/docker/cli-plugins/docker-buildx
COPY --from=fetcher /wrk/docker-compose /usr/libexec/docker/cli-plugins/docker-compose
COPY --from=fetcher /wrk/bin/* /usr/local/bin/

RUN curl -fsSL https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip > /tmp/awscli.zip \
    && unzip /tmp/awscli.zip -d /tmp \
    && sudo ./tmp/aws/install \
    && rm -rf /tmp/aws*

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash - \
    && sudo apt-get install -y nodejs \
    && sudo npm install -g yarn \
    && sudo rm -rf /var/lib/apt/lists/*

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
    && sudo rm -rf /var/lib/apt/lists/*

ENV LANG=C.UTF-8
