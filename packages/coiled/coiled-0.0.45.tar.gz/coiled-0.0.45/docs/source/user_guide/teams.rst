:notoc:

=====
Teams
=====

Coiled helps individuals and teams manage their resources, control costs, and
collaborate with one another.


Using a Team account
--------------------

If you are part of a team, you can create clusters or any other resources in
your team account by using the ``account=`` keyword argument that most of our
:doc:`API commands <api>` accept, or by specifying ``my-team-account-name/``
as a prefix in the ``name=`` keyword argument.

For example, to create a cluster in your team account:

.. code-block:: python

   import coiled

   cluster = coiled.Cluster(n_workers=10, account="my-team-account-name")

Or, to create a software environment in your team account:

.. code-block:: python

   import coiled

   coiled.create_software_environment(
       name="my-team-account-name/my-pip-env",
       pip=["dask[complete]", "xarray==0.15.1", "numba"],
   )

Alternatively, you can also update your
:doc:`local coiled configuration file <configuration>` and add your team account
name in this file to always use your team account when you are using coiled.


Sharing
-------

Software environments and cluster configurations which belong to an account are
visible and accessible to all account members. This allows team members to
easily control, share, and collaborate on their teams's resources.


Accounts & teams
----------------

`Upon signing up <https://coiled.typeform.com/to/mu6Inr4S>`_, each Coiled user
is automatically given their own personal account (the account name is the same
as their username) which they can use to manage software environments, create
cluster configurations, and launch Dask clusters.

Additionally, organizations and other teams can create their own Coiled account
and add existing Coiled users to their team. Team members can be added and
removed to an account at https://cloud.coiled.io/users. This enables team
members to create software environments, cluster configurations, etc. within a
team's account (instead of their personal account) to easily share resources and
collaborate with other team members.

.. figure:: images/team-management.png


Resource limits & tracking costs
--------------------------------

Administrators for each Coiled account can set resource limits for account
members like the number of cores a user can allocate at one time or whether or
not to grant access to GPUs (which can be expensive). Additionally, you can
track each cluster's cost over time.

.. figure:: images/clusters-table.png
