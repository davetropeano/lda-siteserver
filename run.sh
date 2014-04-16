#!/bin/sh
set PYTHONPATH=./src:../lda-clientlib/python:../lda-serverlib/mongodbstorage:../lda-serverlib/logiclibrary:$PYTHONPATH
python test/site_server_test.py