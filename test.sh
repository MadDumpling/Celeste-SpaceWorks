#!/usr/bin/env bash

source .venv/bin/activate
export QT_QPA_PLATFORM=offscreen
pytest -v