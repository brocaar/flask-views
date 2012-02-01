#!/usr/bin/env bash

coverage erase
coverage run --omit "*tests*" -m unittest discover
coverage report

