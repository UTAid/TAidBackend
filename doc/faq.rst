FAQ
===

Why are my changes to the calender not visible?
-----------------------------------------------
It might be because some information might be cached in your browser. To fix it
in Google Chrome press ``Ctrl + F5`` to wipe the cache. The problem should
hopefully be fixed.

What database does this app use?
--------------------------------
This app uses SQLite database to store all the information.

What does FSET mean?
--------------------
FSET stands for Filterable, Searchable, Editable Table and this is what the frontend is.

What are the main folders I need to be concerned about?
-------------------------------------------------------
* ``_dev_docs`` - contains code reviews and also the UML of the database
* ``_test_files`` - contains code to create csv test files and also contains
                    already created test files for various courses to populate
                    database with csv files
* ``apps`` - contains the main app. It contains the rest api, calender etc.
* ``doc`` - contains documentation of the app and is here to hopefully answer questions.
* ``run`` - contains database and the files the database holds
* ``static`` - static files like css, js etc
* ``TAid`` - Django related stuff

In rest api I only want to disply the x number elements?
-------------------------------------------------------
This can be done placing the limit and offset tags. Limit gives you the
x number elements and offset causes to skip the first x elements.
Some examples of the url are - http://127.0.0.1:8000/api/v0/students/?limit=20 ,
http://127.0.0.1:8000/api/v0/students/?limit=20&offset=20
