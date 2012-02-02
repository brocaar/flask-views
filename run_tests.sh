#!/usr/bin/env bash

coverage erase
coverage run --include "*flask_views*" --omit "*tests*" -m unittest discover
coverage report

