#!/usr/bin/env bash

coverage erase
coverage run --include "*flask_views*" --omit "*tests*" -m unittest2 discover
coverage report
