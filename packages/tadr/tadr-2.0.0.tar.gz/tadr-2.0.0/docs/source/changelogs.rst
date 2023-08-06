Changelogs
===========

A list of changelogs for TADR, with the most recent version first. These are also available `here <https://github.com/MurdoMaclachlan/tadr/releases>`_.

2.0.0 - Current Release
-----------------------

**Functionality**

- Added and enforced refresh token authentication.
- Refactored Logger.

**Cleanup/Optimisation**

- Optimised ``Static.define_paths()``.
- General optimisations for the rest of the program.

**Dependencies**

- Removed colored.
- Updated praw to 7.5.0.

**Documentation/Logs**

- Added docstrings.
- Updated readthedocs documentation.
- Changed name of ``core`` folder to ``tadrcore`` so pip installation doesn't explode. (#3)

1.0.2
-----

**Cleanup/Optimisation**:

- General small cleanup and readability improvements.

**Bug Fixes**:

- #1: Import error: cannot import ``getTime()`` (fixed in #2).

1.0.1
-----

**Documentation**:

- TADR now logs a full link to messages it replies to, allowing them to be opened by clicking on them in many consoles.

1.0.0
-----

**Meta**:

- Created PIP package, GitHub repository and readthedocs hosting.

**Functionality**:

- Created initial program.
