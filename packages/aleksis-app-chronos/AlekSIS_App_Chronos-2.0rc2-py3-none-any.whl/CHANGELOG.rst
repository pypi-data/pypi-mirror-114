Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_,
and this project adheres to `Semantic Versioning`_.

`2.0rc2`_ - 2021-08-01
----------

Fixed
~~~~~

* Drop usage of non-existing permission in permission rules for lesson substitutions.

`2.0rc1`_ - 2021-06-23
----------------------

Changed
~~~~~~~

* Use semantically correct html elements for headings and alerts.

`2.0b3`_ - 2021-06-16
----------

Changed
~~~~~~~

* Use a more speaking name for preference section ("Timetables" instead of "Chronos").

Fixed
~~~~~

* Preference section verbose names were displayed in server language and not
  user language (fixed by using gettext_lazy).
* Affected groups and persons in substitutions list were displayed multiple times.
* ``lessons_on_day`` didn't work as expected if a person has no lessons.
* End of validity ranges list wasn't detected correctly in ``next_lesson``.

`2.0b2` - 2021-06-02
--------------------

Fixed
~~~~~

* Migration path was ambigious
* Unique constraints for breaks and substitutions were too tight
* Absences in substitutions list were displayed multiple times.

`2.0b1`_ - 2021-05-22
---------------------

Fixed
~~~~~

* Fix migration names and dependencies

`2.0b0`_ - 2021-05-21
---------------------

Added
~~~~~

* Introduce validity range and link data to validity ranges.
* Add option to link subjects to groups
* Add search indices for rooms.
* Show week version of smart timetable on desktop devices.
* Add PDF export function for regular timetables.

Changed
~~~~~~~

* Link week-related models not only to weeks, but also to years.
* Optimise query count in timetable views.
* Go to next week if current day is out of range (weekly timetable view).
* Summarize double lessons in substitutions print view.
* Show only parent groups in "Affected groups".

Fixed
~~~~~

* Do not show dates in regular timetable.
* Show correct tooltip for rooms in substitution table.
* Show extra lessons in which a person is the new teacher in "My timetable".
* Show translations for weekdays.
* Show absent teachers in substitutions plan.
* Show supervisions in substitutions plan.
* Sort teacher short names alphabetically.
* Sort substitutions table by parent groups if displaying parent groups is activated.
* Make previous/next lesson API functions independent of the validity range.
* Show only regular elements in regular timetable, don't include information like holidays.

`2.0a2`_ - 2020-05-04
---------------------

Added
~~~~~

* Header box with absent and affected teachers and groups.
* Provide smart plan for current day as dashboard widget.
* Roles and permissions for timetable and lists.
* Show events in timetable.
* Show exams in timetable.
* Show holidays in timetable.
* Show supervision substitutions in timetable and list.

Changed
~~~~~~~

* Improve handling of different types (substitutions, timetables,…).
* Improve view for groups in timetable views.
* More intelligent personal timetable (checks if current person is teacher,…).
* Show announcements in timetable views.
* Devs: Move prev/next function to models.
* Devs: Rename field abbrev to short_name.

Fixed
~~~~~

* Force all lessons in timetable to same height.
* Render empty periods correctly.

`2.0a1`_ - 2020-02-01
---------------------

Added
~~~~~

* Migrate to MaterializeCSS

Changed
~~~~~~~

* Redesign filter ui for rooms, classes or teachers.
* Rename person timetabe for current day to "smart plan".

Fixed
~~~~~

* Catch error if no timetable data is available.


`1.0a3`_ - 2019-11-24
---------------------

Added
~~~~~

* Add list of all future substitutions.
* Devs: Add API to get date of a period.


`1.0a2`_ - 2019-11-11
---------------------

Added
~~~~~

* Devs: LessonPeriod now has a custom QuerySet and manager for advanced filtering.

Fixed
~~~~~

* Room plan includes substituted lessons now.


`1.0a1`_ - 2019-09-17
---------------------

Added
~~~~~

* Support lesson cancellation.
* Devs: Add fully pythonic API for calendar weeks.

Fixed
~~~~~

* Redirect to correct date after editing a substitution.
* Correctly display teachers for substituted lessons.
* Use bootstrap buttons everywhere.

.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html

.. _1.0a1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/1.0a1
.. _1.0a2: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/1.0a2
.. _1.0a3: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/1.0a3
.. _2.0a1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.0a1
.. _2.0a2: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.0a2
.. _2.0b0: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.0b0
.. _2.0b1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.0b1
.. _2.0b2: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.0b2
.. _2.0b3: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.0b3
.. _2.0rc1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.0rc1
.. _2.0rc2: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.0rc2
