# Changelog

## 1.1.2 - 2025-06-12

### 🚀 Features

* Have HDateInfo API return builtins (str/int) for easier use (#211) @tsvi
* Improve performance of HolidayDatabase creation and lookup (#216) @tsvi

## 1.1.1 - 2025-06-11

### 🚀 Features

* Improve HDateInfo object creation performance by caching and lazy-loading (#215) @tsvi

## 1.1.0 - 2025-04-26

* Unpin astral dependency (#207) @tsvi

### 💥 Breaking

* Change the API for setting the language (#205) @tsvi

### 🚀 Features

* Add implementation for erev shabbat and chag (#200) @tsvi

### 🐛 Bug Fixes

* Refactor moving holidays calculation (#209) @tsvi

## 1.0.3 - 2025-02-16

* Finish updating Zmanim nomenclature (#198) @tsvi

### 🐛 Bug Fixes

* Improve coverage (#199) @tsvi

## 1.0.2 - 2025-02-10

### 🐛 Bug Fixes

* Fix entries of multiple holidays returning inconsistent ordering in HolidayDatabase.get_all_names() (#196) @tsvi

## 1.0.1 - 2025-02-06

### 💥 Breaking

* Rename HDate object to HDateInfo to better reflect its relationship to HebrewDate (#195) @tsvi
* Add diaspora argument to get_all_holiday_names (#191) @tsvi
* Rename Zmanim keys and standardize nomenclature (#190) @tsvi

### 🚀 Features

* Rename HDate object to HDateInfo to better reflect its relationship to HebrewDate (#195) @tsvi
* Type language as literal for actual values (#194) @tsvi
* Cleanup Tekufot and add it to the HDate object (#192) @tsvi

## 1.0.0 - 2025-02-02

* Final reorganization of Parasha API (#180) @tsvi
* Create minimal documentation (#173) @tsvi

### 💥 Breaking

* Simplify holidays API (#164) @tsvi
* Improve Zmanim API (#160) @tsvi
* Change Zmanim to use TranslatorMixin (#153) @tsvi
* Multilanguage (#144) @DanBendavid

### 🚀 Features

* Separate Daf Yomi API (#179) @tsvi
* Separate Holiday API (#175) @tsvi
* Streamline Zmanim API (#176) @tsvi
* Make astral a real optional dependency (#174) @tsvi
* Remove heb_date from HDate API (#170) @tsvi
* Improve test clarity and performance (#169) @tsvi
* HebrewDate API: make Months behave more intuitively (#167) @tsvi
* Create Omer API (#165) @tsvi
* Add prayer and tekufot (#162) @DanBendavid
* Simplify holidays API (#164) @tsvi
* Improve HebrewDate API (#163) @tsvi
* Improve Zmanim API (#160) @tsvi
* Make day prefix part of translation string for dow (#159) @tsvi
* Remove unneeded Location **repr** (#158) @tsvi
* Reorganize code: separate gematria into a separate module (#157) @tsvi
* Move Days to use TranslatorMixin (#156) @tsvi
* Move Parshiyot to use TranslatorMixin (#155) @tsvi
* Change Zmanim to use TranslatorMixin (#153) @tsvi
* Use translations.py instead of JSON files for performance (#152) @tsvi
* Support language propagation (#151) @tsvi
* Use TranslatorMixin for Holidays (#150) @tsvi
* Change Daf Yomi to use TranslatorMixin (#148) @tsvi
* Use TranslatorMixin class for Months (#147) @tsvi
* Multilanguage (#144) @DanBendavid
* Add support for night according to Rabenou Tam and mincha gedola according to 30 min (#142) @DanBendavid

### 🐛 Bug Fixes

* Fix Italian Omer Nusach (#168) @tsvi
* Fix Shabbat after Hag Candle Lighting time (#145) @DanBendavid

## 0.11.1 - 2024-11-14

### 🚀 Features

* Add helper method for all holiday options (#143) @tsvi

### 🐛 Bug Fixes

* Fix is_holiday behavior (#140) @tsvi

## 0.11.0 - 2024-11-12

### 🚀 Features

* Make libhdate fully typed (#136) @tsvi
* Add Rosh Chodesh holiday (#129) @tsvi

### 🐛 Bug Fixes

* 30th of Kislev should also be considered chanuka (#135) @tsvi

### 🧰 Maintenance

* Deprecate support for Python 3.8, add support for Python 3.13 (#134) @tsvi

## 0.10.11 - 2024-06-21

### 🧰 Maintenance

* Fix changelog not updating and commit not being pushed in release flow (#128) @tsvi

## 0.10.10 - 2024-06-21

### 🧰 Maintenance

* Cleanup the release flow (#127) @tsvi
* Cleanup unnecessary code (#126) @tsvi
* Use PEP-459 compatible built-in ZoneInfo (#125) @tsvi

## 0.10.9 - 2024-6-18

* Allow locations to the north of 50 degrees latitude (#124) @tsvi
* Use PDM as our package manager (#123) @tsvi
* add Is leap year method (#120) @aviadlevy

## 0.10.8 - 2024-3-11

* Revert minimal astral version to 2.2

## 0.10.7 - 2024-3-9

* Fix publishing part of workflow

## 0.10.6 - 2024-1-30

* Update Github actions
* Fix dependabots issues
* Fix issues with get_holidays_for_year() (#117)
* Update .readthedocs.yaml to latest required spec
* add Python 3.11 testing to tox and remove 3.7 (#115)
* use-dict-literal (#114)
* use dataclass for HebrewDate (#110)
* Bump certifi from 2022.9.24 to 2022.12.7 (#109)
* Fix spelling (#108)
* Move development to 3.7 by default (#107)
* Some more cleanups due to python2 deprecation (#105)
* Drop support for Python 2 (#101)
* Add french language support (#103)
* Update packages to latest supported python version
* Minor nitpick when printing Zmanim times
* Cleanup py2 semantics
* Remove linting from tox (part of pre-commit)
* Update requirements to python 3.7

## 0.10.2 - 2020-12-27

* Use environment files instead of set-env
* Fix version in pyproject.toml and fix github release flow (#84)
* Move to poetry (#83)

## 0.10.0 - 2020-11-2

* Use astral in Zmanim time calculations (#79)
* Setup read the docs configuration (#81)
* Initial commit for working with Sphinx for documentation (#80)

## 0.9.12 - 2020-10-26

* issur_melacha should include candle_lighting (#78)
* Add Python 3.9 to CI (#77)
* Update README.rst and Fixes some typos (#75)
* Fix instructions for setting up development environment (#73)

## 0.9.11 - 2020-7-22

* Terminate sed command
* Fix missing closing quote (#70)
* Fix sed search and replace for version number (#69)
* Update workflows based on other projects (#68)
* fix: Don't run tests on master (#64)
* chore: Add auto-release workflow action (#63)
* fix: Allow user to trigger tests on their forked branch as well (#62)
* Use checkout v1 as v2 is broken with creation of PR (#60)
* Use repo-sync instead of peter evans create pull request action (#59)
* Fix: Use specific deploy label (#58)
* Use regex match for label name (#57)
* fix: when updating changlelog push back to pull request (#56)
* fix: Minor typos - test changelog generation (#55)
* chore: add support for automatic changelog generation (#54)
* Fix(devops): run_tests workflow
* style: Fix dev docs formatting
* fix(ci): Pass correct Git credentials before running semantic-release
* fix(ci): Forgot to specify the GitHub actions in tox.ini
* chores(ci): Make contributions easier with pre-commit hooks and GH actions
* docs: Update development guide
* chore: Implement CI using Github actions
* chore(devops): Implement pre-commit
* chore(devops): Move to use semantic release instead of bumpversion

## 0.9.7 - 2020-02-23

* Use Travis repo environment variable. @tsvi
* Fix deployment, temporarily remove on.tags. @tsvi

## 0.9.6 - 2020-02-23

* Add automatic deployment. @tsvi

## 0.9.5 - 2020-01-22

### Fix

* Small lint fixes and pass tests on python2.7. @tsvi

## 0.9.4 - 2020-01-22

* Merge pull request #46 from moshekaplan/master. @tsvi
  Add daf yomi to hdate
  
* Rename daf_yomi properties to be more intuitive. @moshekaplan
  
* Make suggested improvements. @moshekaplan
  
* Add daf yomi to a date. @moshekaplan
  

## 0.9.3 - 2019-10-31

* Lower verbosity of holiday calculations. @tsvi

## 0.9.2 - 2019-10-31

* Remove logger statement. @tsvi

## 0.9.1 - 2019-10-16

* Fix requirements for python 2.7. @tsvi
  
* Make tox -e check pass after blackifying. @tsvi
  
* Blackify hdate. @tsvi
  
* Use official enum implementation for Months and HolidayTypes. @tsvi
  
* Fix test in case of shabbat rosh hashana. @tsvi
  
* Remove support for Python 3.5 in tox and travis. @tsvi
  
* Don't use f-strings. @tsvi
  We still support Python 2
  
* Add tests for parshiot around rosh hashana. @tsvi
  
* Fix for Parshat shavua on last weeks of year. @tsvi
  

## 0.9.0 - 2019-08-06

* Accept timezone aware datetime as an argument to Zmanim. @tsvi
  
* Move from dateutil to pytz. @tsvi
  
  dateutil requires the system to have timezone files. When homeassistant runs
  as a docker image these are not available, and timezone is set to tzlocal().
  
  To handle the timezones properly we're moving to use pytz instead
  
* Remove pylintrc from manifest. @tsvi
  
* Add logging and comments to zmanim. @tsvi
  
* Refactor utc_minute_timezone method as utc_zmanim dictionary. @tsvi
  
  The UTC zmanim dictionary holds the zmanim in UTC format
  
* Use UTC time internally when doing calculations. @tsvi
  
* Merge pull request #43 from tsvi/master. @tsvi
  
  Bump version: 0.8.7 → 0.8.8
  

## 0.8.8 - 2019-07-02

* Merge pull request #42 from tsvi/master. @tsvi
  Remove unnecessary import
  
* Remove unnecessary import. @tsvi
  
* Merge pull request #41 from tsvi/master. @tsvi
  
  Rewrite issur_melacha_in_effect
  
* Merge pull request #1 from tsvi/fix-issur-melacha. @tsvi
  
  Rewrite issur_melacha_in_effect
  
* Rewrite issur_melacha_in_effect. @tsvi
  
  Rewrite the function in terms of havdala and candle lighting time.
  
  This might fix
  
  * #home-assistant/23032
  * #home-assistant/24479
  * #home-assistant/23852
  

## 0.8.7 - 2018-12-18

* Split tests so they're a bit more readable, to help us fix #36. @tsvi
* Family day has only existed as a national holiday since 1974. @tsvi
* Cleanup whitespace errors. @tsvi

## 0.8.6 - 2018-12-18

* Merge pull request #37 from arigilder/upcoming. @tsvi
  
  Add additional properties for upcoming shabbat+yomtov, zmanim, & more
  
* Address review comments. @arigilder
  
* Fix comments. @arigilder
  
* Fix spacing. @arigilder
  
* Strip whitespace. @arigilder
  
* Add better multi-day yomtov support to issur_melacha property. @arigilder
  
* Lint fixes. @arigilder
  
* Add additional properties for YT and Shabbat candles/havdalah and
  first/last days. @arigilder
  

## 0.8.5 - 2018-12-13

* Merge pull request #35 from arigilder/readings. @tsvi
  
  Fix bugs with readings, sub-HDates, etc.
  
* Merge fix from HEAD. @arigilder
  
* Lint fixes. @arigilder
  
* Fix some reading bugs (+cleanup), propagate diaspora/hebrew to sub-
  HDates. @arigilder
  

## 0.8.4 - 2018-12-09

* Revert greedy removal of pylint warning. @tsvi
  
  For class inheritance to work correctly under python 2, we need BaseClass to
  inherit from object. Therefore we also need to add the pylint disabling of
  useless-object-inheritance.
  
  Python 2 tests pass now.
  

## 0.8.3 - 2018-12-09

* Remove and update pylint warnings. @tsvi
  
  Some warnings are for Python 2.7 only. As long as the code runs on Python2.7 we don't care
  about the linter warnings. They are tested w.r.t. Python 3.
  
  Also add six dependency, and disable TODO warnings in pylint.
  
  When running pylint on it's own it should get caught.
  
* Merge pull request #34 from arigilder/upcoming_shabbat. @tsvi
  
  A few lint fixes I forgot to commit
  
* A few lint fixes I forgot to commit. @arigilder
  
* Merge pull request #33 from arigilder/upcoming_shabbat. @tsvi
  
  Add functions for identifying upcoming shabbat and Yom Tov
  
* Lint fixes and other changes for review. @arigilder
  
* Add newline. @arigilder
  
* Add is_holiday property, some lint cleanup. @arigilder
  
* Add docstrings. @arigilder
  
* Add next shabbat and next yom tov + some refactoring. @arigilder
  
* Add upcoming shabbat and yom tov properties and tests. @arigilder
  
* Merge pull request #32 from arigilder/cleanup. @tsvi
  
  Add enums for Months and other small cleanup
  
  Thanks
  
* Cleanup linter checks. @tsvi
  
* Add memorial day holiday type. @arigilder
  
* Fix import ordering. @arigilder
  
* Add enums for Months and other cleanup. @arigilder
  
* Give the sources for the Zmanim calculations in the docstrings. @tsvi
  

## 0.8.2 - 2018-11-25

* Change and add erev chagim to all be of holiday_type == 2. @tsvi
  
  Erev shavuot had a holiday type of 9 which doesn't match other holiday_type 9.
  Other chagim didn't have any erev chagim specified except for erev yom kippur
  which was holiday_type 2.
  
  Unfortuantely with the current code, this doesn't simplify the check for issur_melacha
  as in the case of diaspora the first day yom tov is holiday_type 1, maybe holiday type
  should be a list instead of an int. Call it holiday properties. This would allow
  hoshana raba to be defined as chol hamoed, erev yom tov and special.
  
* Add support for setting the shabbes offset. @tsvi
  

## 0.8.1 - 2018-11-22

* Remove holiday indices as they're superfluous. @tsvi
  
  The old system used indices to lookup properties baout the holidays. As holidays
  are now defined by namedtuples, there's no point in storing indices or using them as
  "magic numbers".
  
  The only place where the indices were used in the code were tests, so the test have
  been updated accordingly.
  
* Add direct tests on conversion methods to get better test coverage.
  @tsvi
  
* Rename test variables. @tsvi
  
* Add converters test file. @tsvi
  
* Test with correct holiday name spelling. @tsvi
  
* Improve coverage and simplify some tests. @tsvi
  
* Implement  a placeholder for the **unicode** method of BaseClass
  objects. @tsvi
  
* Some more code deduplication. @tsvi
  
* Remove duplicate code. @tsvi
  
* Fix flake8 errors. @tsvi
  
* Reorder imports according to isort rules. @tsvi
  
* Add test for typerror case for Zmanim. @tsvi
  
* Cause check to run with python 3.6 on travis. @tsvi
  
* Add tests for erev shaabat and erev Yom tov. @tsvi
  
* Should cause Travis to run linters as well. @tsvi
  
* Fix double negation in inequality testing. @tsvi
  
* Return the copied object not the generator. @tsvi
  
* Fix fixture not returning internal function. @tsvi
  
* Fix original not passed to deepcopy fixture. @tsvi
  
* Fixes missing fixture statement. @tsvi
  
* Fixes common tests. @tsvi
  
* Consolidate tests. @tsvi
  
* Implement **repr** function for Zmanim and Location objects. @tsvi
  
* Print the seconds output for zmanim. @tsvi
  
  This simplifies the logic for printing the Zmanim object as a
  string.
  BREAKING CHANGE
  
* Fix test passing although not testing. @tsvi
  
* Improve test coverage for edge cases. @tsvi
  
* Add test for repr implementation and fix implementation. @tsvi
  

## 0.8.0 - 2018-11-12

* Fix tox.ini to allow running specific tests via tox. @tsvi
  
* Implement tests and fix bugs for issur_melacha_in_effect. @tsvi
  
* Add Zmanim property for issur_melacha. @tsvi
  
* Remov unnecessary typechecking. Not pythonic. @tsvi
  
* When printing the HDate represantation, return the gdate `repr` @tsvi
  
* Zmanim should simply be a property, that way no assignment of
  get_zmanim is necessary. @tsvi
  
* Move utc_minute_timezone to be closer to othe code calulcations. @tsvi
  
* Move type checking to property setters. @tsvi
  
  Not really sure about this, as it inflates the code.
  
* Remove the Zmanim object from the HDate object. @tsvi
  
  Based on some discussion I read this would not be healthy as it creates a G-D object.
  A smarter move would be instead to create either a third class that would wrap both, or else
  even better might be to create a property that would instantiate a zmanim object and check
  the given time in relationship to the times from the Zmanim object.
  
  Another option would be to create it as a property of the Zmanim object which would instantiate
  a HDate object.
  
* Add docstrings and pylint disable warnings. @tsvi
  
* Breaking change: Update README example and update the test
  accordingly. @tsvi
  
* Change Location from namedtuple into a proper class. @tsvi
  
* Get most tests to pass. @tsvi
  
* Fix cyclic dependency. @tsvi
  
  This commit causes the tests to run again. Doesn't pass yet.
  
* Move `get_zmanim_string` to be the implementation of `__unicode__`  of
  the Zmanim object. @tsvi
  
* Use a dict comprehension for get_zmanim() @tsvi
  
  was using a combersome method of creating two dictionaries. The first one
  to get the values in  UTC time, and the second one to 'massage' the values into the local
  time for the given keys.
  
  This change simplifies the method by using a dict_comprehension instead.
  
* Initial work. @tsvi
  

## 0.7.5 - 2018-11-07

* Cleanup setup.py due to changes in hierarchy. @tsvi

## 0.7.3 - 2018-11-07

* Typo in README.rst. @tsvi

## 0.7.2 - 2018-11-06

* Implement HDate **repr** method. @tsvi

## 0.7.1 - 2018-11-06

* Bring back holiday_name. @tsvi
* Deprecate get_hebrew_date and incorporate it to simply the result of
  **unicode** for the HDate object. @tsvi

## 0.7.0 - 2018-11-06

* Update README and create a test checing for the README's output to be
  valid. @tsvi
  
* Performance enhancements. @tsvi
  
* Make all tests pass. @tsvi
  
* Tox -e check passes again. @tsvi
  
* Cleanup results from linters. @tsvi
  
* Fix paths. @tsvi
  
* Initial work on fixing hdate_set_hdate to use properties. @tsvi
  
* Base on travis-ci#9815, fix travis.yml to get python 3.7 testing as
  well. @tsvi
  
* Forgot to update travis.yml as well. @tsvi
  
* Python 3.7 is stable since June 2018. Add it to tox. @tsvi
  
* Update comment. @tsvi
  
* Cleanup holiday description. @tsvi
  
* Whitespace cleanup. @tsvi
  
* Fix Unicode strings for python 2.7 in tests. @tsvi
  
* Start using logging. @tsvi
  
* Have get_reading return the correct result for weekdays. @tsvi
  
* Pass a datetime object to gdate_to_jdn. @tsvi
  
* Use  @property properly. @tsvi
  
* Add parasha property. @tsvi
  
* Update cheshvan to the correct naming: marcheshvan. @tsvi
  
* Add new API tests and start getting them to pass. @tsvi
  
* Move tox -e check to use python 3.6. @tsvi
  
* Merge pull request #27 from tsvi/master. @tsvi
  
  Bring in lost fix for parasha and tests for timezones
  
* Merge pull request #26 from tsvi/master. @tsvi
  
  Add support for adding providing timezone as a datetime object
  
* Merge pull request #24 from tsvi/master. @tsvi
  
  Reorg of files in preparation for simplification of API
  

## 0.6.5 - 2018-10-16

* Add tests for timezone usage in hdate. @tsvi
* Bring back lost fix for missing parasha. @tsvi

## 0.6.3 - 2018-10-16

* Add possibility to specify timezone as a datetime.tzinfo object. @tsvi
* Add a second ` for markup to be interpreted correctly. @tsvi
* Add documentation for development and allow for easy installation of
  publishing tools. @tsvi

## 0.6.2 - 2018-09-06

* Use bumpversion for updating version numbers. @tsvi
* Make coverage combine optional (in case no coverage exists) @tsvi
* Make isort non-verbose. @tsvi
* Change isort not to require single line imports. @tsvi
* Remove irrelevant gitignores. @tsvi
* Reorganize files in a more logical fashion. @tsvi

## 0.6 - 2017-12-19

* Merge pull request #22 from tsvi/master. @tsvi
  
  Update README to reflect changes done in #20
  
* Update readme to refelect changes. @tsvi
  
* Merge pull request #20 from tsvi/namedtuples. @tsvi
  
  Use namedtuples instead of lists and dicts
  
  This closes #14, #15 and #12
  
* Move parashe to namedtuple. @tsvi
  
* Fix string/unicode representation in Python 2/3. @tsvi
  
* Add get_holyday_name method. @tsvi
  
* Use tuple for description and language. @tsvi
  
* Change lists to tuples. The data in htables is immutable. @tsvi
  
* Simplify code: namedtuples are still tuples. @tsvi
  
* Move MONTHS to namedtuple. @tsvi
  
* Move DAYS to namedtuples. @tsvi
  
* Remove Gregorian months not in use. @tsvi
  
* Use a single list comprehension instead of calling helper functions.
  @tsvi
  
* Fix coverage reporting issues. @tsvi
  
* Update travis.yml for python3 and coveralls support. @tsvi
  
* Remove more pylint warnings as well as code unused due to refactoring
  of get_reading() @tsvi
  
* Refactor get_reading into a simple lookup table. @tsvi
  
* Make year_size a method instead of a class variable. @tsvi
  
* Fix erronuous search and replace. @tsvi
  
* Change _weekday from being a variable to a method dow() @tsvi
  
* Show that python3 is supported in README. @tsvi
  
* Rename _variables to variables so as to remove warnings regarding
  accessing protected variables. @tsvi
  
* Make all tests pass (add tests for yom ha'atsmaut and yom hazikaron)
  @tsvi
  
* Fix for case of  Yom Hashoa. @tsvi
  
* Add some comments explaining the code. @tsvi
  
* Refactor get_holydays and start implementing lambda functions for
  special cases. @tsvi
  
  This commit is not complete yet as tests are known to fail
  
* Add to HOLIDAYS table info for refactoring of get_holyday. @tsvi
  
* Change package layout for better testability. @tsvi
  
* Simplify get_holyday_type method now that type is part of HOLYDAYS
  namedtuple. @tsvi
  
* Insert correct holiday type in HOLIDAYS table. @tsvi
  
* Move HOLIDAYS table to namedtuple and rename ZMAN and ZMANIM. @tsvi
  
* Use ZMANIM_TUPLE instead of lists and dicts. @tsvi
  
* Add tests to pylint checks. @tsvi
  

## 0.5 - 2017-09-12

* Create 0.5 version for critical bugfix in Zmanim. @tsvi
* Bugfix for Zmanim due to move to python 3. @tsvi
* Add setup.cfg for creation of universal wheel. @tsvi

## 0.4 - 2017-09-11

* Update package to version 0.4 which includes python 3 support. @tsvi
  
* Merge pull request #11 from tsvi/py3. @tsvi
  
  Adding python 3 support
  
* Fix **repr** under python 2.7. @tsvi
  
* Remove dependency on future. @tsvi
  
* Remove from unnecessary from builtins import ... @tsvi
  
* Fix missed divisions by futurize. @tsvi
  
* Fix unicode issues after futurize. @tsvi
  
* Cleanup linter and whitespace errors introduced by future. @tsvi
  
* Create python 3 branch after auto-translating with future. @tsvi
  
* Add python3 to list of environments. @tsvi
  

## 0.3 - 2017-09-10

* Merge pull request #10 from tsvi/dev. @tsvi
  
  More unittests and multiple bugfixes
  
* Update README.rst. @tsvi
  
* Update README.rst. @tsvi
  
* Prepare for 0.3 release. @tsvi
  
* Cover all possible year combinations. @tsvi
  
* Revert "Remove lines of code which will never be reached" @tsvi
  
  This reverts commit b4e9dad804591d6ec217711766e4686be65d3577.
  Actually one line will be reached so added it back in
  
* Remove lines of code which will never be reached. @tsvi
  
* Add more tests for get_reading() @tsvi
  
* Add test for get_reading on weekday. @tsvi
  
* Add 5778 to get_reading() test. @tsvi
  
* Start testing of get_reading() function. @tsvi
  
* Fix in test: edge case this_date is 29.02 of leap year. @tsvi
  
* Add full coverage to get_hebrew_number. @tsvi
  
* Bugfix for get_parashe in case user requests English, not short would
  return None. @tsvi
  
  Was found using included unittests
  
* Move holidays tests into a separate class. @tsvi
  
* Fix flake8 errors. @tsvi
  
* Move sanity check for hebrew date to input of date, not when querying
  get_holiday() @tsvi
  
  This gives get_holiday() 100% coverage
  
* Add tests specific for Adar holidays (dealing with multiple Adars and
  Chanuka on 3rd of Tevet. @tsvi
  
* Change last elif case into else for better coverage. @tsvi
  
* Bugfix for omer string in case of tens only - 20, 30) etc. @tsvi
  
* Fix flake8 errors. @tsvi
  
* Add unittests for Zmanim. @tsvi
  
* Remove case of Zhabotinsky day falling on Shabbat. @tsvi
  
  Although the letter of the law specifies that in such case the day is
  to be held on Sunday, such a case can never happen, as 29th of Tamuz
  can only happen on Sunday, Tuesday, Thursday and Friday.
  
* More bugfixes for holiday corner cases. @tsvi
  
* Add pytest.ini to ignore distribution file list. @tsvi
  
* Add options for looponfail. @tsvi
  
* Fix testcases testing days before range. @tsvi
  
* Fix unittest ranges. @tsvi
  
* Bugfix for Zhabotinsky day: there's no such thing as 30'th of Tamuz.
  @tsvi
  
* Add unittests for more dates. @tsvi
  
* Add tests for diaspora yom tov. @tsvi
  
* DRY: split and generalize tests for get_holiday() @tsvi
  
* Bugfix: hebrew number == 0 should raise an error as well. @tsvi
  
* Disregard calling coveralls in tox exit status. @tsvi
  
* Fix for flake8. @tsvi
  
* Bugfix: in case of values over 1000, add a geresh + space after the
  thousands. @tsvi
  
* Add unittests for hebrew_number() @tsvi
  
* Fix flake8 failures. @tsvi
  
* Bugfix for get_omer_string() @tsvi
  
* Add tests for omer day strings. @tsvi
  
* Merge pull request #5 from tsvi/master. @royi1000
  
  Add tests for holyday type and omer day and some small code refactoring
  
* Fix comment. @tsvi
  
* Add support for coveralls. @tsvi
  
* .pylintrc does not need to be distibuted with manifest. @tsvi
  
* .pylintrc. @tsvi
  
* Test all the different holidays for get_holyday_type. @tsvi
  
* Add --cov-branch option to tox.ini. @tsvi
  
* Add more unittests for shalosh regalim. @tsvi
  
* Remove unnecessary method. @tsvi
  
* Add exception for linter and some better comments. @tsvi
  
* Revert "Refactor calculation of molad for a shorter and more readable
  'if' statement" @tsvi
  
  This reverts commit 7623b425ca1b3b9ee516e61298ef3d62d92fd284.
  
* Add tests for omer day and refactor code. @tsvi
  
* Simplify some of the code, rename `jd_`, `_jd`, `jday` and `jdate` to `jdn`. @tsvi
  
* Refactor calculation of molad for a shorter and more readable 'if'
  statement. @tsvi
  
* Refactor get_holiday function to cleanup multiple return statements. @tsvi
  
* Remove unused class attribute. @tsvi
  
* Merge pull request #4 from tsvi/master. @royi1000
  
  Sorry for such a large pull request
  
* Refactor code so all values are initialized in **init** of HDate. @tsvi
  
* Add htmlcov to .gitignore. @tsvi
  
* Add test for the vaious holidays. @tsvi
  
* Fix flake8 and pydocstyle errors. @tsvi
  
* Setting hdate or setting gdate all class variables should be the same. @tsvi
  
* Bugfix: when initalizing using hdate_set_hdate, set the class hdate. @tsvi
  
* Test for first day of rosh hashana and pesach. @tsvi
  
* Rename function for disambiguation. @tsvi
  
* Add more tests for year size. @tsvi
  
* Add testing for length of year. @tsvi
  
* Add flake8 tests to tests. @tsvi
  
* Add HDate tests for weekday. @tsvi
  
* Cleanup error too-many-local-variables. @tsvi
  
* Remove unnecesary else after return (unpythonic) @tsvi
  
* Move get_holyday_type out of class. @tsvi
  
* Finish cleaning up invalid-name errors in pylint. @tsvi
  
* Add first py.test tests. @tsvi
  
* Add check for MANIFEST.in. @tsvi
  
* Fix typo. @tsvi
  
* Add python version supported. @tsvi
  
  Currently only 2.7 is supported.
  
* Fix typo. @tsvi
  
* Add pydocstyle tests and implement fixes in docstrings. @tsvi
  
* Add docstrings. @tsvi
  
* Rename jd variable to jday. @tsvi
  
* Fix use of relative imports. @tsvi
  
* Fix tox basepython. @tsvi
  
* Remove from travis unsupported python versions. @tsvi
  
* Remove hdate_julian executable permissions. @tsvi
  
* Update gitignore with more venv files. @tsvi
  
* Fix indentation. @tsvi
  
* Rename jd variable to fix variable name length. @tsvi
  
* Add docstring for htables module. @tsvi
  
* Rename private function names to fix lint errors. @tsvi
  
* Rename constants so they match python naming convention. @tsvi
  
* Cleanup a few short variable names. @tsvi
  
* Cleanup whitespace. @tsvi
  
* Fix bugs, use of bad variable and accidentally unused variable. @tsvi
  
* Remove redundant code. @tsvi
  
* Remove original C source code. @tsvi
  
* Remove unused duplicate code. @tsvi
  
* Merge branch 'master' of [https://github.com/royi1000/py-libhdate]. @tsvi
  
* Merge pull request #1 from tsvi/master. @royi1000
  Cleanup of flake8 errors and a small fix to README so it shows up more clearly
  
* Cleanup variable names for better compliance with pylint. @tsvi
  
* Add Travis CI YAML file. @tsvi
  
* Cleanup code based on pylint recommendations. @tsvi
  
* Update .gitignore. @tsvi
  
* Add tox.ini for tests. @tsvi
  
* Edit whitespaces in table. @tsvi
  
* Update markdown to show code python console text correctly. @tsvi
  
* Fix all flake8 errors. @tsvi
  
* Fix flake8 errors (except line to long) @tsvi
  
* Add omer string. @royi1000
  
* First pypi upload. @royi1000
  
* Add strings. @royi1000
  
* Move tables to diffrent file. @royi1000
  
* Move tables to diffrent file. @royi1000
  
* Add more zmanim. @royi1000
  
* Add Zmanim. @royi1000
  
* Fix .gitignore to include `*.pyc`. @royi1000
  
* Fix syntex error. @royi1000
  
* Fix syntex errors. @royi1000
  
* Add sun times. @royi1000
  
* Add julian. @royi1000
  
* First commit. @royi1000
  
