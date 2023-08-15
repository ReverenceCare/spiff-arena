Spiffworkflow Backend
==========
|Tests| |Codecov| |pre-commit| |Black|

.. |Tests| image:: https://github.com/sartography/spiffworkflow-backend/workflows/Tests/badge.svg
   :target: https://github.com/sartography/spiffworkflow-backend/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/sartography/spiffworkflow-backend/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/sartography/spiffworkflow-backend
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black

Features
--------

* Backend API portion of the spiffworkflow engine webapp


Running Locally
---------------

* Add a folder called instance in the src folder
* Add a config.py file in the src/instance folder.
* Add the following settings to the config.py file:
   FLASK_SESSION_SECRET_KEY = "Only the good die young"
   SPIFFWORKFLOW_BACKEND_BPMN_SPEC_ABSOLUTE_DIR = '/the/full/path/to/your/demo-process-models'
   SPIFFWORKFLOW_BACKEND_RUN_BACKGROUND_SCHEDULER = True
   SPIFFWORKFLOW_BACKEND_OPEN_ID_SERVER_URL = 'http://localhost:7000/openid'
   SPIFFWORKFLOW_BACKEND_PERMISSIONS_FILE_NAME = 'example.yml'
   SPIFFWORKFLOW_BACKEND_LOG_LEVEL = "DEBUG"
   SPIFFWORKFLOW_BACKEND_BACKGROUND_SCHEDULER_POLLING_INTERVAL_IN_SECONDS=50

* After installing the poetry, you can start the backend with:
.. code:: console

   $ FLASK_ENV="local_development" poetry run flask run -p 7000
   
* Install libraries using poetry:

.. code:: console

   $ poetry install

* Setup the database - uses mysql and assumes server is running by default:

.. code:: console

   $ ./bin/recreate_db clean

* Run the server:

.. code:: console

   $ ./bin/run_server_locally


Requirements
------------

* Python 3.10+
* Poetry


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `MIT license`_,
*Spiffworkflow Backend* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.

.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT license: https://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/sartography/spiffworkflow-backend/issues
.. _pip: https://pip.pypa.io/
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
.. _Usage: https://spiffworkflow-backend.readthedocs.io/en/latest/usage.html
