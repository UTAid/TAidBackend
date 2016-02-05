Code review - 2015-01-31
========================

__Reviewer__: Edouard

__Branch__: API

__Purpose__: API Code Review

General Comments
-------------------
- In general looks ok, but without proper documentation it can be very hard
to follow what is going on.

- We no longer care about course code as this will run per course instance.
Should be updated to reflect that.

- I hope I am on the right branch................

TAid/settings/common.py
---------------------------
- Nothing to say about this.

TAid/urls.py
--------------
- A good idea to add a docstring detailing where the verious routes are
defined.

apps/taid/serializers.py
----------------------------
- Needs to be updated to remove course code.

apps/taid/viewsets.py
------------------------
- Needs to be updated to remove course code.

apps/taid/models.py
----------------------
- As this file gets more filled up, maybe it might be a good idea to 
split the verious classes into different python files.

- Remove courses.

- In addition to the diagram, there needs to be a section in the 
docs detailing some of the SQL relations of the db. (Which will explain
the models better.)

apps/taid/parsers.py
-----------------------
- Add #TODO for empty functions (or implement them or remove them if 
unneeded)