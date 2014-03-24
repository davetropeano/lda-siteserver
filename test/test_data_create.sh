#!/bin/bash
export PYTHONPATH=.:../src:../libs/MongoDBStorage:../libs/LogicLibrary 
export APP_NAME=siteserver
export MONGODB_DB_HOST=localhost
export MONGODB_DB_PORT=27017
python create_test_data.py