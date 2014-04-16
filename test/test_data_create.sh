#!/bin/bash
set PYTHONPATH=.:../../lda-clientlib/python:../../lda-clientlib/python/test:$PYTHONPATH
python create_test_data.py "$1"