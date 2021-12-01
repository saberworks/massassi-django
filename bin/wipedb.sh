#!/bin/bash
set -euxo pipefail

# WIPE DATABASE
find ../ -path '*/migrations/*' -regex ".*/[0-9]+.*" -delete
find ../ -name '*.pyc' -delete

dropdb -h db -p 5432 -U massassi massassi
createdb -h db -p 5432 -U massassi --owner=massassi massassi
