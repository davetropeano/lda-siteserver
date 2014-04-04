lda-siteserver
==============

This project contains the siteserver application which provides standard system functions for LDA applications, specifically
authentication, access control and multi-tenancy.

`Note: if you don't have python 2.7, you need to install it before proceeding.`

**The siteserver application requires a running MongoDB database server and Nginx reverse proxy server to function.**
You can start these severs any way you want, but the easiest way to start properly configured servers for testing is using
the Vagrantfile provided in the **lda-examples** project.
See [Downloading the Software](http://ld4apps.github.io/downloading-the-software/index.html) for instructions.

To run the siteserver application, proceed as follows:

1. Start a mongodb and nginx server, if you haven't already done so:

        cd lda-examples # we're assuming you've also downloaded the lda-examples repository from github
        vagrant up
        
2. cd into the siteserver project root directory:

        cd lda-siteserver


3. Get the required python libraries (only needs to be run once):

        python setup.py install


4. Run the siteserver application:

        ./run.sh (or equivalent for your OS)

   You should see the message "test site server initiated on host: localhost port: 3005".

5. Create test data (optional):

        cd test
        ./test_data_create.sh

   If successful, you should see a couple of messages on the console:

        ######## POSTed resource: http://localhost:3001/account/explorer, status: 201
        ######## POSTed resource: http://localhost:3001/account/admin, status: 201

You should now be able to point your browser at http://localhost:3001/, the home page of the hosting site. The test data includes 
a user, "admin" (with corresponding password "admin"), that you can use to login with.

The multi-tenant hosting support in lda-siteserver is designed to run behind a properly configured DNS server.
Because we are currently just running on 'localhost', before you can create new sites, you'll need to add some lines
in your /etc/hosts (C:\Windows\System32\Drivers\etc\hosts on Windows) file [on your host machine] corresponding to the name(s)
you plan to give your site(s). 
For example:

        127.0.0.1 testsite.localhost
        127.0.0.1 cloudsupplements.localhost

Note: 'cloudsupplements' is the name of the site used in 'Setupshop sample' in the [lda-examples](https://github.com/ld4apps/lda-examples)
repository.
 