FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
  python3-dev python3-pip \
  libx11-6 libx11-dev x11-utils \
  libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
  libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /workspaces/FIA

# COPY requirements.txt .

# RUN pip install -r requirements.txt
