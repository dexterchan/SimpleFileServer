#!/usr/bin/env bash

PRJ=abcd

DOCKER_IMAGE_NAME=gcr.io/$PRJ/simplefileserver:v1


docker build -t $DOCKER_IMAGE_NAME  .