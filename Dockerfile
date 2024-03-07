FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3.11 \
    pipx \
    && pipx install poetry \
    && pipx ensurepath
    