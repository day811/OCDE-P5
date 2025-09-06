#!/bin/bash

export $(grep -v '^#' .test.env | xargs)

docker-compose up -d mongo