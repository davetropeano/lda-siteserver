lda-siteserver
==============

This project contains the siteserver application which provides standard system functions for LDA applications, specifically
authentication, access control and multi-tenancy.

`
Note: if you don't have python 2.7, you need to install it before proceeding.
`

The siteserver application requires a running MongoDB database server and Nginx reverse proxy server to function. 
The easiest way to start properly configured servers is using the Vagrantfile provided in the **lda-examples** project.
See [Getting Started](http://ld4apps.github.io/getting-started/index.html).

Once you've started the MongoDB and Nginx servers, you can run siteserver as follows:

1. cd into the siteserver project root directory:
```sh
cd lda-siteserver
```

1. Get the required python libraries (only needs to be run once):
```sh
python setup.py install
```

1. Run the siteserver application:
```sh
./run.sh (or equivalent for your OS)
```
You should see the message "test site server initiated on host: localhost port: 3005".

1. Create test data (optional):
```sh
cd test
./test_data_create.sh
```
If successful, you should see a couple of messages on the console:
```sh
######## POSTed resource: http://localhost:3001/account/explorer, status: 201
######## POSTed resource: http://localhost:3001/account/admin, status: 201
```

You should now be able to point your browser at http://localhost:3001/, the home page of the hosting site. The test data includes 
a user, "admin" (with corresponding password "admin"), that you can use to login with.

The multi-tenant hosting support in lda-siteserver is designed to run behind a properly configured DNS server.
Because we are currently just running on 'localhost', before you can create new sites, you'll need to add some lines
in your /etc/hosts (C:\Windows\System32\Drivers\etc\hosts on Windows) file [on your host machine] corresponding to the name(s)
you plan to give your site(s). 
For example:

```sh
127.0.0.1 testsite.localhost
127.0.0.1 cloudsupplements.localhost
```

Note: 'cloudsupplements' is the name of the site used in **setupshop sample** in the [lda-examples](https://github.com/ld4apps/lda-examples) repository.
 