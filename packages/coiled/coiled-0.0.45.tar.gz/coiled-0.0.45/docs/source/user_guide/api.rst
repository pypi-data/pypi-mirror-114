=============
API Reference
=============

.. panels::
   :body: text-center

    :opticon:`file-code,size=24`

    .. link-button:: python-api
        :type: ref
        :text: Python API Reference
        :classes: btn-full btn-block stretched-link

    ---

    :opticon:`terminal,size=24`

    .. link-button:: command-line-api
        :type: ref
        :text: Command Line API Reference
        :classes: btn-full btn-block stretched-link


.. _python-api:

Python API Reference
====================

.. currentmodule:: coiled

.. autosummary::
    coiled.Cluster
    coiled.cluster_cost_estimate
    coiled.cluster_logs
    coiled.create_cluster_configuration
    coiled.create_job_configuration
    coiled.create_notebook
    coiled.create_software_environment
    coiled.delete_cluster
    coiled.delete_cluster_configuration
    coiled.delete_job_configuration
    coiled.delete_software_environment
    coiled.diagnostics
    coiled.get_notifications
    coiled.get_software_info
    coiled.install
    coiled.job_logs
    coiled.list_cluster_configurations
    coiled.list_clusters
    coiled.list_core_usage
    coiled.list_job_configurations
    coiled.list_jobs
    coiled.list_local_versions
    coiled.list_performance_reports
    coiled.list_software_environments
    coiled.list_user_information
    coiled.performance_report
    coiled.set_backend_options
    coiled.start_job
    coiled.stop_job

Software Environments
---------------------
.. autofunction:: coiled.create_software_environment
.. autofunction:: coiled.delete_software_environment
.. autofunction:: coiled.get_software_info
.. autofunction:: coiled.inspect
.. autofunction:: coiled.install
.. autofunction:: coiled.list_software_environments


Cluster Configurations
----------------------
.. autofunction:: coiled.create_cluster_configuration
.. autofunction:: coiled.delete_cluster_configuration
.. autofunction:: coiled.list_cluster_configurations


Clusters
--------
.. autoclass:: coiled.Cluster
    :members:
    :undoc-members:

.. autofunction:: coiled.cluster_cost_estimate
.. autofunction:: coiled.cluster_logs
.. autofunction:: coiled.delete_cluster
.. autofunction:: coiled.list_clusters
.. autofunction:: coiled.list_core_usage


Performance Reports
-------------------
.. autofunction:: coiled.list_performance_reports
.. autofunction:: coiled.performance_report


Notebooks
---------
.. autofunction:: coiled.create_notebook


Jobs
----
.. autofunction:: coiled.create_job_configuration
.. autofunction:: coiled.delete_job_configuration
.. autofunction:: coiled.job_logs
.. autofunction:: coiled.list_job_configurations
.. autofunction:: coiled.list_jobs
.. autofunction:: coiled.start_job
.. autofunction:: coiled.stop_job


Backend
-------
.. autofunction:: coiled.set_backend_options


Information
-----------
.. autofunction:: coiled.diagnostics
.. autofunction:: coiled.get_notifications
.. autofunction:: coiled.list_local_versions
.. autofunction:: coiled.list_user_information


.. _command-line-api:

Command Line API Reference
==========================

.. click:: coiled.cli.login:login
   :prog: coiled login
   :show-nested:

.. _coiled-install-api:

.. click:: coiled.cli.install:install
   :prog: coiled install
   :show-nested:

.. click:: coiled.cli.env:create
   :prog: coiled env create
   :show-nested:

.. click:: coiled.cli.env:delete
   :prog: coiled env delete
   :show-nested:

.. click:: coiled.cli.env:list
   :prog: coiled env list
   :show-nested:

.. click:: coiled.cli.env:inspect
   :prog: coiled env inspect
   :show-nested:
