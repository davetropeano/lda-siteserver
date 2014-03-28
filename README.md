lda-siteserver
==============

This project contains the siteserver application which provides standard system functions for LDA applications, specifically
authentication, access control and multi-tenancy.

`
Note: if you don't have python 2.7, you need to install it before proceeding.
`

The siteserver application requires a running MongoDB database server and Nginx reverse proxy server to function. 
The easiest way to start properly configured servers is using the Vagrantfile provided in the **lda-examples** project. See [Getting Started](http://davetropeano.github.io/lda/getting-started/index.html).

Once you've started the MongoDB and Nginx servers, you can run siteserver as follows:

1. Get the required python libraries (only needs to be done once):
```sh
python setup.py install
```
1. Run the siteserver application:
```sh
./run.sh (or equivalent for your OS)
```
You should see the message "test site server initiated on host: localhost port: 3005".
1. Create test data:
```sh
cd test
./test_data_create.sh
```

You should now be able to point your browser at http://localhost:3001/, the home page of the hosting site.
