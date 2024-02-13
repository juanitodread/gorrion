#!/bin/bash

flake8 || exit
pytest -vv || exit
