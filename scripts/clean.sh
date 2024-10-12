#!/usr/bin/env bash

rm -rf venv
find . -type d -name ".DS_Store" -exec rm -rf {} +
find . -type d -name "__pycache__" -exec rm -rf {} +
