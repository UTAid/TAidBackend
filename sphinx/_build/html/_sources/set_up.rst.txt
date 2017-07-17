Set up Documentation
============================

**TAid** is an application for managing grades and courses. Developed
for Anya Tafliovich at UTSC.

Requirements
------------

Can be found at ``requirements.txt``

.. literalinclude:: ../requirements.txt

Installation
------------

It is recommended to have ``pip`` and ``virtualenvwrapper`` setup on
your base machine for development. Clone this repo to your destination.
Just run ``pip install -r requirments.txt`` inside of a virtualenv to
download all your dependencies.

Set-up
~~~~~~

The code uses python2. Follow the instructions to setup a local server
in your machine:

- ``sudo apt-get install python-pip`` - This will install pip

- ``sudo pip2 install -r requirements.txt`` - This will install all the dependencies found in the requirements.txt file

- ``python2 manage.py makemigrations`` - Creates new migrations based on the changes you have made to your models (placed here just to be cautious)

- ``python2 manage.py migrate`` - Applies the migrations and sets up the database

- ``python2 manage.py createsuperuser`` - Sets up an admin user (follow instructions on screen)

- ``python2 manage.py runserver`` - This sets up a development server on the local pc

Exploring the development server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The development server will most likely will be set as
``http://127.0.0.1:8000/`` but if otherwise it will say so on the screen
when ``python2 manage.py runserver`` is run

- ``http://127.0.0.1:8000/admin/`` will take to the admin page. Put in the credentials that were made during the set-up process

- ``http://127.0.0.1:8000/api/v0/`` will take to the api page. If not logged in, click on login button top right corner of screen and provide admin credentials.

  - Now going to ``http://127.0.0.1:8000/api/v0/`` will show more information on the screen of the links where different API requests can be made

  - Now going to ``http://127.0.0.1:8000/api/v0/docs/`` will show the operations available to the rest api

Documentation
~~~~~~~~~~~~~
Documentation of the overall project can be found at:

``sphinx/_build/html/index.html``
