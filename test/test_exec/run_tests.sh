#!/bin/bash

#set location to lda-examples/setupshop
cd ../..

# start siteserver and direct output to log file
cd ../../lda-siteserver
nohup sh run.sh > ~/site_server_test.log &

# wait for servers to come up
sleep 10

# create test data for siteserver
cd test
echo 'travis_fold:start:siteserver_testdata'
echo 'siteserver_testdata create'
sh test_data_create.sh
echo 'travis_fold:end:siteserver_testdata'

# execute tests
cd test_exec
py.test
pytest_result=$?

# TODO: kill servers

# output siteserver log
echo 'travis_fold:start:site_server_test.log'
echo 'site_server_test output'
cat ~/site_server_test.log
echo 'travis_fold:end:site_server_test.log'

# return py.test result
exit ${pytest_result}