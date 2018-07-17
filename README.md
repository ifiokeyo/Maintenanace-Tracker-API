Maintenanace-Tracker-API
========================

An API for the maintenance/Repair tracker app.


Development setup
-----------------

- Clone this repo and navigate into the project's directory

  .. code-block:: console

     $ git clone https://github.com/ifiokeyo/Maintenanace-Tracker-API && cd maint_tracker

- Create a ``python3`` virtual environment for the project and activate it.

  - To install ``python3`` on OSX you can
    `follow this <http://python-guide-pt-br.readthedocs.io/en/latest/starting/install3/osx/>`_

  - To install the virtual environment wrapper ``mkvirtualenv`` you can
    `follow this <https://jamie.curle.io/installing-pip-virtualenv-and-virtualenvwrapper-on-os-x>`_.

  .. code-block:: console

     $ mkvirtualenv --py=python3 maint_tracker

- Install the project's requirements

  .. code-block:: console

     $ pip install -r requirements.txt


- Copy ``.env_sample`` into ``.env`` in the ``server`` directory which is inside the base folder of the project.
  You should adjust it according to your own local settings. To set up
  ``postgres`` database locally you can
  `follow this <http://exponential.io/blog/2015/02/21/install-postgresql-on-mac-os-x-via-brew/>`_.

- Run database upgrade

  .. code-block:: console

     $ flask db upgrade

- Run the app:

  .. code-block:: console
     $ cd server

     $ python main.py

- Run tests:

  .. code-block:: console
     $ cd test

     $ python -m unittest


- The app should now be available from your browser at ``http://127.0.0.1:9000``

- To send the API requests on Postman, you can click `follow this <https://www.getpostman.com/docs/postman/sending_api_requests/requests>`_.

Making Changes to the Model
---------------------------

- After making a change on the model, apply the database migration to make the change in the database before pushing the code on Github:

  .. code-block:: console

     $ flask db migrate -m “message indicating change made”

  .. code-block:: console

     $ flask db upgrade

- Check migrations history to confirm change is made.

  .. code-block:: console

     $ flask db history

Applying Migrations after Pull Rebasing
---------------------------------------

- When branches have been merged to the main branch and you have run ```git pull -r```, run the upgrade command to incorporate new changes to the database schema.

  .. code-block:: console

     $ flask db upgrade

Resolving Schema Conflicts
--------------------------
- Schema conflicts will occur when a merge is done and different changes to the model were done in different branches.

- Run the merge command to create another migration that merges multiple heads.

  .. code-block:: console

     $ flask db merge -m "merge migrations from branches"

- Upgrade the database.

  .. code-block:: console

     $ flask db upgrade

- Save and run ```flask db history``` to confirm it has been reordered.

