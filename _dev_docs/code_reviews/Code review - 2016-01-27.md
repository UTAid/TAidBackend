Code review - 2016-01-27
========================

__Reviewer__: Leo

__Branch__: API

__Purpose__: Review database related code


General Comments
----------------
- Source files lack headers to give general summary of file's purpose.
Something like what is done within the scripts in /settings is OK.

- Are there any DB design files? Would be nice to have that linked in the
README. Not only to get me familiarized, but also for future reference.

- Although code is very self-explanatory, there should be some comments on
the general purpose of classes/models (what they aim to accomplish).

admin.py
--------
- Some comments to explain why certain things are stacked-in-line, or excluded.

models.py
---------
- Maybe mark empty models with a #TODO comment

- line 43: Should provide some comments as to why length has to be 254.
	- also on line 72

- Currently having Tutorial and Practical models seem too be redundant. It may
be a design decision that hasn't been fully realized, but comments should
explain that.

- Some comments is needed to explain purpose of models. Either that, or a
design file.

parsers.py
----------
- line 10: Nothing seems to be done with student.

tests.py
--------

- No tests!? 

serializers.py
--------------

- Some comments to explain why certain fields are serialized vs not serialized
would be nice.

Questions
---------
- Not sure what line 17 is doing in parsers.py Is it creating a new entry in the
database without using save()?

- What is the advantage of using a HyperlinkedModelSerializer over a standard 
ModelSerializer?