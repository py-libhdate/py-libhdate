Changelog
=========


(unreleased)
------------
- Fix(ci): Pass correct Git credentials before running semantic-release.
  [Tsvi Mostovicz]

  fix(ci): Pass correct Git credentials before running semantic-release
- Fix(ci): Pass correct Git credentials before running semantic-release.
  [Tsvi Mostovicz]
- Fix(ci): Forgot to specify the GitHub actions in tox.ini. [Tsvi
  Mostovicz]

  fix(ci): Forgot to specify the GitHub actions in tox.ini
- Fix(ci): Forgot to specify the GitHub actions in tox.ini. [Tsvi
  Mostovicz]
- Docs: Update development guide. [Tsvi Mostovicz]


v0.9.7 (2020-02-23)
-------------------
- Use Travis repo environment variable. [Tsvi Mostovicz]
- Fix deployment, temporarily remove on.tags. [Tsvi Mostovicz]


v0.9.6 (2020-02-23)
-------------------
- Add automatic deployment. [Tsvi Mostovicz]


v0.9.5 (2020-01-22)
-------------------

Fix
~~~
- Small lint fixes and pass tests on python2.7. [Tsvi Mostovicz]


v0.9.4 (2020-01-22)
-------------------
- Merge pull request #46 from moshekaplan/master. [Tsvi Mostovicz]

  Add daf yomi to hdate
- Rename daf_yomi properties to be more intuitive. [Moshe Kaplan]
- Make suggested improvements. [Moshe Kaplan]
- Add daf yomi to a date. [Moshe Kaplan]


v0.9.3 (2019-10-31)
-------------------
- Lower verbosity of holiday calculations. [Tsvi Mostovicz]


v0.9.2 (2019-10-31)
-------------------
- Remove logger statement. [Tsvi Mostovicz]


v0.9.1 (2019-10-16)
-------------------
- Fix requirements for python 2.7. [Tsvi Mostovicz]
- Make tox -e check pass after blackifying. [Tsvi Mostovicz]
- Blackify hdate. [Tsvi Mostovicz]
- Use official enum implementation for Months and HolidayTypes. [Tsvi
  Mostovicz]
- Fix test in case of shabbat rosh hashana. [Tsvi Mostovicz]
- Remove support for Python 3.5 in tox and travis. [Tsvi Mostovicz]
- Don't use f-strings. [Tsvi Mostovicz]

  We still support Python 2
- Add tests for parshiot around rosh hashana. [Tsvi Mostovicz]
- Fix for Parshat shavua on last weeks of year. [Tsvi Mostovicz]


v0.9.0 (2019-08-06)
-------------------
- Accept timezone aware datetime as an argument to Zmanim. [Tsvi
  Mostovicz]
- Move from dateutil to pytz. [Tsvi Mostovicz]

  dateutil requires the system to have timezone files. When homeassistant runs
  as a docker image these are not available, and timezone is set to tzlocal().

  To handle the timezones properly we're moving to use pytz instead
- Remove pylintrc from manifest. [Tsvi Mostovicz]
- Add logging and comments to zmanim. [Tsvi Mostovicz]
- Refactor utc_minute_timezone method as utc_zmanim dictionary. [Tsvi
  Mostovicz]

  The UTC zmanim dictionary holds the zmanim in UTC format
- Use UTC time internally when doing calculations. [Tsvi Mostovicz]
- Merge pull request #43 from tsvi/master. [Tsvi Mostovicz]

  Bump version: 0.8.7 → 0.8.8


v0.8.8 (2019-07-02)
-------------------
- Merge pull request #42 from tsvi/master. [Tsvi Mostovicz]

  Remove unnecessary import
- Remove unnecessary import. [Tsvi Mostovicz]
- Merge pull request #41 from tsvi/master. [Tsvi Mostovicz]

  Rewrite issur_melacha_in_effect
- Merge pull request #1 from tsvi/fix-issur-melacha. [Tsvi Mostovicz]

  Rewrite issur_melacha_in_effect
- Rewrite issur_melacha_in_effect. [Tsvi Mostovicz]

  Rewrite the function in terms of havdala and candle lighting time.

  This might fix
   - #home-assistant/23032
   - #home-assistant/24479
   - #home-assistant/23852


v0.8.7 (2018-12-18)
-------------------
- Split tests so they're a bit more readable, to help us fix #36. [Tsvi
  Mostovicz]
- Family day has only existed as a national holiday since 1974. [Tsvi
  Mostovicz]
- Cleanup whitespace errors. [Tsvi Mostovicz]


v0.8.6 (2018-12-18)
-------------------
- Merge pull request #37 from arigilder/upcoming. [Tsvi Mostovicz]

  Add additional properties for upcoming shabbat+yomtov, zmanim, & more
- Address review comments. [Ari Gilder]
- Fix comments. [Ari Gilder]
- Fix spacing. [Ari Gilder]
- Strip whitespace. [Ari Gilder]
- Add better multi-day yomtov support to issur_melacha property. [Ari
  Gilder]
- Lint fixes. [Ari Gilder]
- Add additional properties for YT and Shabbat candles/havdalah and
  first/last days. [Ari Gilder]


v0.8.5 (2018-12-13)
-------------------
- Merge pull request #35 from arigilder/readings. [Tsvi Mostovicz]

  Fix bugs with readings, sub-HDates, etc.
- Merge fix from HEAD. [Ari Gilder]
- Lint fixes. [Ari Gilder]
- Fix some reading bugs (+cleanup), propagate diaspora/hebrew to sub-
  HDates. [Ari Gilder]


v0.8.4 (2018-12-09)
-------------------
- Revert greedy removal of pylint warning. [Tsvi Mostovicz]

  For class inheritance to work correctly under python 2, we need BaseClass to
  inherit from object. Therefore we also need to add the pylint disabling of
  useless-object-inheritance.

  Python 2 tests pass now.


v0.8.3 (2018-12-09)
-------------------
- Remove and update pylint warnings. [Tsvi Mostovicz]

  Some warnings are for Python 2.7 only. As long as the code runs on Python2.7 we don't care
  about the linter warnings. They are tested w.r.t. Python 3.

  Also add six dependency, and disable TODO warnings in pylint.

  When running pylint on it's own it should get caught.
- Merge pull request #34 from arigilder/upcoming_shabbat. [Tsvi
  Mostovicz]

  A few lint fixes I forgot to commit
- A few lint fixes I forgot to commit. [Ari Gilder]
- Merge pull request #33 from arigilder/upcoming_shabbat. [Tsvi
  Mostovicz]

  Add functions for identifying upcoming shabbat and Yom Tov
- Lint fixes and other changes for review. [Ari Gilder]
- Add newline. [Ari Gilder]
- Add is_holiday property, some lint cleanup. [Ari Gilder]
- Add docstrings. [Ari Gilder]
- Add next shabbat and next yom tov + some refactoring. [Ari Gilder]
- Add upcoming shabbat and yom tov properties and tests. [Ari Gilder]
- Merge pull request #32 from arigilder/cleanup. [Tsvi Mostovicz]

  Add enums for Months and other small cleanup

  Thanks
- Cleanup linter checks. [Tsvi Mostovicz]
- Add memorial day holiday type. [Ari Gilder]
- Fix import ordering. [Ari Gilder]
- Add enums for Months and other cleanup. [Ari Gilder]
- Give the sources for the Zmanim calculations in the docstrings. [Tsvi
  Mostovicz]


v0.8.2 (2018-11-25)
-------------------
- Change and add erev chagim to all be of holiday_type == 2. [Tsvi
  Mostovicz]

  Erev shavuot had a holiday type of 9 which doesn't match other holiday_type 9.
  Other chagim didn't have any erev chagim specified except for erev yom kippur
  which was holiday_type 2.

  Unfortuantely with the current code, this doesn't simplify the check for issur_melacha
  as in the case of diaspora the first day yom tov is holiday_type 1, maybe holiday type
  should be a list instead of an int. Call it holiday properties. This would allow
  hoshana raba to be defined as chol hamoed, erev yom tov and special.
- Add support for setting the shabbes offset. [Tsvi Mostovicz]


v0.8.1 (2018-11-22)
-------------------
- Remove holiday indices as they're superfluous. [Tsvi Mostovicz]

  The old system used indices to lookup properties baout the holidays. As holidays
  are now defined by namedtuples, there's no point in storing indices or using them as
  "magic numbers".

  The only place where the indices were used in the code were tests, so the test have
  been updated accordingly.
- Add direct tests on conversion methods to get better test coverage.
  [Tsvi Mostovicz]
- Rename test variables. [Tsvi Mostovicz]
- Add converters test file. [Tsvi Mostovicz]
- Test with correct holiday name spelling. [Tsvi Mostovicz]
- Improve coverage and simplify some tests. [Tsvi Mostovicz]
- Implement  a placeholder for the __unicode__ method of BaseClass
  objects. [Tsvi Mostovicz]
- Some more code deduplication. [Tsvi Mostovicz]
- Remove duplicate code. [Tsvi Mostovicz]
- Fix flake8 errors. [Tsvi Mostovicz]
- Reorder imports according to isort rules. [Tsvi Mostovicz]
- Add test for typerror case for Zmanim. [Tsvi Mostovicz]
- Cause check to run with python 3.6 on travis. [Tsvi Mostovicz]
- Add tests for erev shaabat and erev Yom tov. [Tsvi Mostovicz]
- Should cause Travis to run linters as well. [Tsvi Mostovicz]
- Fix double negation in inequality testing. [Tsvi Mostovicz]
- Return the copied object not the generator. [Tsvi Mostovicz]
- Fix fixture not returning internal function. [Tsvi Mostovicz]
- Fix original not passed to deepcopy fixture. [Tsvi Mostovicz]
- Fixes missing fixture statement. [Tsvi Mostovicz]
- Fixes common tests. [Tsvi Mostovicz]
- Consolidate tests. [Tsvi Mostovicz]
- Implement __repr__ function for Zmanim and Location objects. [Tsvi
  Mostovicz]
- Print the seconds output for zmanim. [Tsvi Mostovicz]

  This simplifies the logic for printing the Zmanim object as a
  string.
  BREAKING CHANGE
- Fix test passing although not testing. [Tsvi Mostovicz]
- Improve test coverage for edge cases. [Tsvi Mostovicz]
- Add test for repr implementation and fix implementation. [Tsvi
  Mostovicz]


v0.8.0 (2018-11-12)
-------------------
- Fix tox.ini to allow running specific tests via tox. [Tsvi Mostovicz]
- Implement tests and fix bugs for issur_melacha_in_effect. [Tsvi
  Mostovicz]
- Add Zmanim property for issur_melacha. [Tsvi Mostovicz]
- Remov unnecessary typechecking. Not pythonic. [Tsvi Mostovicz]
- When printing the HDate represantation, return the gdate `repr` [Tsvi
  Mostovicz]
- Zmanim should simply be a property, that way no assignment of
  get_zmanim is necessary. [Tsvi Mostovicz]
- Move utc_minute_timezone to be closer to othe code calulcations. [Tsvi
  Mostovicz]
- Move type checking to property setters. [Tsvi Mostovicz]

  Not really sure about this, as it inflates the code.
- Remove the Zmanim object from the HDate object. [Tsvi Mostovicz]

  Based on some discussion I read this would not be healthy as it creates a G-D object.
  A smarter move would be instead to create either a third class that would wrap both, or else
  even better might be to create a property that would instantiate a zmanim object and check
  the given time in relationship to the times from the Zmanim object.

  Another option would be to create it as a property of the Zmanim object which would instantiate
  a HDate object.
- Add docstrings and pylint disable warnings. [Tsvi Mostovicz]
- Breaking change: Update README example and update the test
  accordingly. [Tsvi Mostovicz]
- Change Location from namedtuple into a proper class. [Tsvi Mostovicz]
- Get most tests to pass. [Tsvi Mostovicz]
- Fix cyclic dependency. [Tsvi Mostovicz]

  This commit causes the tests to run again. Doesn't pass yet.
- Move `get_zmanim_string` to be the implementation of `__unicode__`  of
  the Zmanim object. [Tsvi Mostovicz]
- Use a dict comprehension for get_zmanim() [Tsvi Mostovicz]

  was using a combersome method of creating two dictionaries. The first one
  to get the values in  UTC time, and the second one to 'massage' the values into the local
  time for the given keys.

  This change simplifies the method by using a dict_comprehension instead.
- Initial work. [Tsvi Mostovicz]


v0.7.5 (2018-11-07)
-------------------
- Cleanup setup.py due to changes in hierarchy. [Tsvi Mostovicz]


v0.7.3 (2018-11-07)
-------------------
- Typo in README.rst. [Tsvi Mostovicz]


v0.7.2 (2018-11-06)
-------------------
- Implement HDate __repr__ method. [Tsvi Mostovicz]


v0.7.1 (2018-11-06)
-------------------
- Bring back holiday_name. [Tsvi Mostovicz]
- Deprecate get_hebrew_date and incorporate it to simply the result of
  __unicode__ for the HDate object. [Tsvi Mostovicz]


v0.7.0 (2018-11-06)
-------------------
- Update README and create a test checing for the README's output to be
  valid. [Tsvi Mostovicz]
- Performance enhancements. [Tsvi Mostovicz]
- Make all tests pass. [Tsvi Mostovicz]
- Tox -e check passes again. [Tsvi Mostovicz]
- Cleanup results from linters. [Tsvi Mostovicz]
- Fix paths. [Tsvi Mostovicz]
- Initial work on fixing hdate_set_hdate to use properties. [Tsvi
  Mostovicz]
- Base on travis-ci#9815, fix travis.yml to get python 3.7 testing as
  well. [Tsvi Mostovicz]
- Forgot to update travis.yml as well. [Tsvi Mostovicz]
- Python 3.7 is stable since June 2018. Add it to tox. [Tsvi Mostovicz]
- Update comment. [Tsvi Mostovicz]
- Cleanup holiday description. [Tsvi Mostovicz]
- Whitespace cleanup. [Tsvi Mostovicz]
- Fix Unicode strings for python 2.7 in tests. [Tsvi Mostovicz]
- Start using logging. [Tsvi Mostovicz]
- Have get_reading return the correct result for weekdays. [Tsvi
  Mostovicz]
- Pass a datetime object to gdate_to_jdn. [Tsvi Mostovicz]
- Use  @property properly. [Tsvi Mostovicz]
- Add parasha property. [Tsvi Mostovicz]
- Update cheshvan to the correct naming: marcheshvan. [Tsvi Mostovicz]
- Add new API tests and start getting them to pass. [Tsvi Mostovicz]
- Move tox -e check to use python 3.6. [Tsvi Mostovicz]
- Merge pull request #27 from tsvi/master. [Tsvi Mostovicz]

  Bring in lost fix for parasha and tests for timezones
- Merge pull request #26 from tsvi/master. [Tsvi Mostovicz]

  Add support for adding providing timezone as a datetime object
- Merge pull request #24 from tsvi/master. [Tsvi Mostovicz]

  Reorg of files in preparation for simplification of API


v0.6.5 (2018-10-16)
-------------------
- Add tests for timezone usage in hdate. [Tsvi Mostovicz]
- Bring back lost fix for missing parasha. [Tsvi Mostovicz]


v0.6.3 (2018-10-16)
-------------------
- Add possibility to specify timezone as a datetime.tzinfo object. [Tsvi
  Mostovicz]
- Add a second ` for markup to be interpreted correctly. [Tsvi
  Mostovicz]
- Add documentation for development and allow for easy installation of
  publishing tools. [Tsvi Mostovicz]


v0.6.2 (2018-09-06)
-------------------
- Use bumpversion for updating version numbers. [Tsvi Mostovicz]
- Make coverage combine optional (in case no coverage exists) [Tsvi
  Mostovicz]
- Make isort non-verbose. [Tsvi Mostovicz]
- Change isort not to require single line imports. [Tsvi Mostovicz]
- Remove irrelevant gitignores. [Tsvi Mostovicz]
- Reorganize files in a more logical fashion. [Tsvi Mostovicz]


0.6 (2017-12-19)
----------------
- Merge pull request #22 from tsvi/master. [Tsvi Mostovicz]

  Update README to reflect changes done in #20
- Update readme to refelect changes. [Tsvi Mostovicz]
- Merge pull request #20 from tsvi/namedtuples. [Tsvi Mostovicz]

  Use namedtuples instead of lists and dicts

  This closes #14, #15 and #12
- Move parashe to namedtuple. [Tsvi Mostovicz]
- Fix string/unicode representation in Python 2/3. [Tsvi Mostovicz]
- Add get_holyday_name method. [Tsvi Mostovicz]
- Use tuple for description and language. [Tsvi Mostovicz]
- Change lists to tuples. The data in htables is immutable. [Tsvi
  Mostovicz]
- Simplify code: namedtuples are still tuples. [Tsvi Mostovicz]
- Move MONTHS to namedtuple. [Tsvi Mostovicz]
- Move DAYS to namedtuples. [Tsvi Mostovicz]
- Remove Gregorian months not in use. [Tsvi Mostovicz]
- Use a single list comprehension instead of calling helper functions.
  [Tsvi Mostovicz]
- Fix coverage reporting issues. [Tsvi Mostovicz]
- Update travis.yml for python3 and coveralls support. [Tsvi Mostovicz]
- Remove more pylint warnings as well as code unused due to refactoring
  of get_reading() [Tsvi Mostovicz]
- Refactor get_reading into a simple lookup table. [Tsvi Mostovicz]
- Make year_size a method instead of a class variable. [Tsvi Mostovicz]
- Fix erronuous search and replace. [Tsvi Mostovicz]
- Change _weekday from being a variable to a method dow() [Tsvi
  Mostovicz]
- Show that python3 is supported in README. [Tsvi Mostovicz]
- Rename _variables to variables so as to remove warnings regarding
  accessing protected variables. [Tsvi Mostovicz]
- Make all tests pass (add tests for yom ha'atsmaut and yom hazikaron)
  [Tsvi Mostovicz]
- Fix for case of  Yom Hashoa. [Tsvi Mostovicz]
- Add some comments explaining the code. [Tsvi Mostovicz]
- Refactor get_holydays and start implementing lambda functions for
  special cases. [Tsvi Mostovicz]

  This commit is not complete yet as tests are known to fail
- Add to HOLIDAYS table info for refactoring of get_holyday. [Tsvi
  Mostovicz]
- Change package layout for better testability. [Tsvi Mostovicz]
- Simplify get_holyday_type method now that type is part of HOLYDAYS
  namedtuple. [Tsvi Mostovicz]
- Insert correct holiday type in HOLIDAYS table. [Tsvi Mostovicz]
- Move HOLIDAYS table to namedtuple and rename ZMAN and ZMANIM. [Tsvi
  Mostovicz]
- Use ZMANIM_TUPLE instead of lists and dicts. [Tsvi Mostovicz]
- Add tests to pylint checks. [Tsvi Mostovicz]


0.5 (2017-09-12)
----------------
- Create 0.5 version for critical bugfix in Zmanim. [Tsvi Mostovicz]
- Bugfix for Zmanim due to move to python 3. [Tsvi Mostovicz]
- Add setup.cfg for creation of universal wheel. [Tsvi Mostovicz]


0.4 (2017-09-11)
----------------
- Update package to version 0.4 which includes python 3 support. [Tsvi
  Mostovicz]
- Merge pull request #11 from tsvi/py3. [Tsvi Mostovicz]

  Adding python 3 support
- Fix __repr__ under python 2.7. [Tsvi Mostovicz]
- Remove dependency on future. [Tsvi Mostovicz]
- Remove from unnecessary from builtins import ... [Tsvi Mostovicz]
- Fix missed divisions by futurize. [Tsvi Mostovicz]
- Fix unicode issues after futurize. [Tsvi Mostovicz]
- Cleanup linter and whitespace errors introduced by future. [Tsvi
  Mostovicz]
- Create python 3 branch after auto-translating with future. [Tsvi
  Mostovicz]
- Add python3 to list of environments. [Tsvi Mostovicz]


0.3 (2017-09-10)
----------------
- Merge pull request #10 from tsvi/dev. [Tsvi Mostovicz]

  More unittests and multiple bugfixes
- Update README.rst. [Tsvi Mostovicz]
- Update README.rst. [Tsvi Mostovicz]
- Prepare for 0.3 release. [Tsvi Mostovicz]
- Cover all possible year combinations. [Tsvi Mostovicz]
- Revert "Remove lines of code which will never be reached" [Tsvi
  Mostovicz]

  This reverts commit b4e9dad804591d6ec217711766e4686be65d3577.
  Actually one line will be reached so added it back in
- Remove lines of code which will never be reached. [Tsvi Mostovicz]
- Add more tests for get_reading() [Tsvi Mostovicz]
- Add test for get_reading on weekday. [Tsvi Mostovicz]
- Add 5778 to get_reading() test. [Tsvi Mostovicz]
- Start testing of get_reading() function. [Tsvi Mostovicz]
- Fix in test: edge case this_date is 29.02 of leap year. [Tsvi
  Mostovicz]
- Add full coverage to get_hebrew_number. [Tsvi Mostovicz]
- Bugfix for get_parashe in case user requests English, not short would
  return None. [Tsvi Mostovicz]

  Was found using included unittests
- Move holidays tests into a separate class. [Tsvi Mostovicz]
- Fix flake8 errors. [Tsvi Mostovicz]
- Move sanity check for hebrew date to input of date, not when querying
  get_holiday() [Tsvi Mostovicz]

  This gives get_holiday() 100% coverage
- Add tests specific for Adar holidays (dealing with multiple Adars and
  Chanuka on 3rd of Tevet. [Tsvi Mostovicz]
- Change last elif case into else for better coverage. [Tsvi Mostovicz]
- Bugfix for omer string in case of tens only (20, 30) etc. [Tsvi
  Mostovicz]
- Fix flake8 errors. [Tsvi Mostovicz]
- Add unittests for Zmanim. [Tsvi Mostovicz]
- Remove case of Zhabotinsky day falling on Shabbat. [Tsvi Mostovicz]

  Although the letter of the law specifies that in such case the day is
  to be held on Sunday, such a case can never happen, as 29th of Tamuz
  can only happen on Sunday, Tuesday, Thursday and Friday.
- More bugfixes for holiday corner cases. [Tsvi Mostovicz]
- Add pytest.ini to ignore distribution file list. [Tsvi Mostovicz]
- Add options for looponfail. [Tsvi Mostovicz]
- Fix testcases testing days before range. [Tsvi Mostovicz]
- Fix unittest ranges. [Tsvi Mostovicz]
- Bugfix for Zhabotinsky day: there's no such thing as 30'th of Tamuz.
  [Tsvi Mostovicz]
- Add unittests for more dates. [Tsvi Mostovicz]
- Add tests for diaspora yom tov. [Tsvi Mostovicz]
- DRY: split and generalize tests for get_holiday() [Tsvi Mostovicz]
- Bugfix: hebrew number == 0 should raise an error as well. [Tsvi
  Mostovicz]
- Disregard calling coveralls in tox exit status. [Tsvi Mostovicz]
- Fix for flake8. [Tsvi Mostovicz]
- Bugfix: in case of values over 1000, add a geresh + space after the
  thousands. [Tsvi Mostovicz]
- Add unittests for hebrew_number() [Tsvi Mostovicz]
- Fix flake8 failures. [Tsvi Mostovicz]
- Bugfix for get_omer_string() [Tsvi Mostovicz]
- Add tests for omer day strings. [Tsvi Mostovicz]
- Merge pull request #5 from tsvi/master. [royi1000]

  Add tests for holyday type and omer day and some small code refactoring
- Fix comment. [Tsvi Mostovicz]
- Add support for coveralls. [Tsvi Mostovicz]
- .pylintrc does not need to be distibuted with manifest. [Tsvi
  Mostovicz]
- .pylintrc. [Tsvi Mostovicz]
- Test all the different holidays for get_holyday_type. [Tsvi Mostovicz]
- Add --cov-branch option to tox.ini. [Tsvi Mostovicz]
- Add more unittests for shalosh regalim. [Tsvi Mostovicz]
- Remove unnecessary method. [Tsvi Mostovicz]
- Add exception for linter and some better comments. [Tsvi Mostovicz]
- Revert "Refactor calculation of molad for a shorter and more readable
  'if' statement" [Tsvi Mostovicz]

  This reverts commit 7623b425ca1b3b9ee516e61298ef3d62d92fd284.
- Add tests for omer day and refactor code. [Tsvi Mostovicz]
- Simplify some of the code, rename jd_, _jd, jday and jdate to jdn.
  [Tsvi Mostovicz]
- Refactor calculation of molad for a shorter and more readable 'if'
  statement. [Tsvi Mostovicz]
- Refactor get_holiday function to cleanup multiple return statements.
  [Tsvi Mostovicz]
- Remove unused class attribute. [Tsvi Mostovicz]
- Merge pull request #4 from tsvi/master. [royi1000]

  Sorry for such a large pull request
- Refactor code so all values are initialized in __init__ of HDate.
  [Tsvi Mostovicz]
- Add htmlcov to .gitignore. [Tsvi Mostovicz]
- Add test for the vaious holidays. [Tsvi Mostovicz]
- Fix flake8 and pydocstyle errors. [Tsvi Mostovicz]
- Setting hdate or setting gdate all class variables should be the same.
  [Tsvi Mostovicz]
- Bugfix: when initalizing using hdate_set_hdate, set the class hdate.
  [Tsvi Mostovicz]
- Test for first day of rosh hashana and pesach. [Tsvi Mostovicz]
- Rename function for disambiguation. [Tsvi Mostovicz]
- Add more tests for year size. [Tsvi Mostovicz]
- Add testing for length of year. [Tsvi Mostovicz]
- Add flake8 tests to tests. [Tsvi Mostovicz]
- Add HDate tests for weekday. [Tsvi Mostovicz]
- Cleanup error too-many-local-variables. [Tsvi Mostovicz]
- Remove unnecesary else after return (unpythonic) [Tsvi Mostovicz]
- Move get_holyday_type out of class. [Tsvi Mostovicz]
- Finish cleaning up invalid-name errors in pylint. [Tsvi Mostovicz]
- Add first py.test tests. [Tsvi Mostovicz]
- Add check for MANIFEST.in. [Tsvi Mostovicz]
- Fix typo. [Tsvi Mostovicz]
- Add python version supported. [Tsvi Mostovicz]

  Currently only 2.7 is supported.
- Fix typo. [Tsvi Mostovicz]
- Add pydocstyle tests and implement fixes in docstrings. [Tsvi
  Mostovicz]
- Add docstrings. [Tsvi Mostovicz]
- Rename jd variable to jday. [Tsvi Mostovicz]
- Fix use of relative imports. [Tsvi Mostovicz]
- Fix tox basepython. [Tsvi Mostovicz]
- Remove from travis unsupported python versions. [Tsvi Mostovicz]
- Remove hdate_julian executable permissions. [Tsvi Mostovicz]
- Update gitignore with more venv files. [Tsvi Mostovicz]
- Fix indentation. [Tsvi Mostovicz]
- Rename jd variable to fix variable name length. [Tsvi Mostovicz]
- Add docstring for htables module. [Tsvi Mostovicz]
- Rename private function names to fix lint errors. [Tsvi Mostovicz]
- Rename constants so they match python naming convention. [Tsvi
  Mostovicz]
- Cleanup a few short variable names. [Tsvi Mostovicz]
- Cleanup whitespace. [Tsvi Mostovicz]
- Fix bugs, use of bad variable and accidentally unused variable. [Tsvi
  Mostovicz]
- Remove redundant code. [Tsvi Mostovicz]
- Remove original C source code. [Tsvi Mostovicz]
- Remove unused duplicate code. [Tsvi Mostovicz]
- Merge branch 'master' of https://github.com/royi1000/py-libhdate.
  [Tsvi Mostovicz]
- Merge pull request #1 from tsvi/master. [royi1000]

  Cleanup of flake8 errors and a small fix to README so it shows up more clearly
- Cleanup variable names for better compliance with pylint. [Tsvi
  Mostovicz]
- Add Travis CI YAML file. [Tsvi Mostovicz]
- Cleanup code based on pylint recommendations. [Tsvi Mostovicz]
- Update .gitignore. [Tsvi Mostovicz]
- Add tox.ini for tests. [Tsvi Mostovicz]
- Edit whitespaces in table. [Tsvi Mostovicz]
- Update markdown to show code python console text correctly. [Tsvi
  Mostovicz]
- Fix all flake8 errors. [Tsvi Mostovicz]
- Fix flake8 errors (except line to long) [Tsvi Mostovicz]
- Add omer string. [royi r]
- First pypi upload. [royi r]
- Add strings. [royi r]
- Move tables to diffrent file. [Royi Reshef]
- Move tables to diffrent file. [Royi Reshef]
- Add more zmanim. [Royi Reshef]
- Add Zmanim. [Royi Reshef]
- Fix .gitignore to include *.pyc. [Royi Reshef]
- Fix syntex error. [Royi Reshef]
- Fix syntex errors. [Royi Reshef]
- Add sun times. [Royi Reshef]
- Add julian. [Royi Reshef]
- First commit. [Royi Reshef]
