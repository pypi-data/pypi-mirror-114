:notoc:

.. _user-guide:

===========
Coiled Docs
===========

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Start Here

   getting_started
   next_steps
   quick_reference

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Using Coiled

   cluster
   software_environment
   backends
   performance_reports
   gpu
   jupyter
   configuration
   teams
   jobs
   notebooks

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Guides

   examples
   tutorials/index
   best_practices
   security

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Help

   support
   faq
   troubleshooting/index

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Reference

   api
   changelog
   oss-foundations

👋 Welcome to Coiled's documentation!

What is Coiled?
---------------

`Coiled <https://coiled.io>`_ provides cluster-as-a-service functionality to
provision hosted Dask clusters on demand. It takes the DevOps out of data
science and enables data engineers and data scientists to spend more time on
their real job and less time setting up networking, managing fleets of Docker
images, creating AWS IAM roles, etc.

.. panels::
   :card: border-0
   :container: container-lg pb-3
   :column: col-md-4 col-md-4 col-md-4 p-2
   :body: text-center border-0
   :header: text-center border-0 h4 bg-white
   :footer: border-0 bg-white

   Hosted Dask Clusters
   ^^^^^^^^^^^^^^^^^^^^

   Securely deploy Dask clusters from anywhere you run Python.

   +++

   .. link-button:: cluster
      :type: ref
      :text: Learn more
      :classes: btn-full btn-block stretched-link

   ---


   Software Environments
   ^^^^^^^^^^^^^^^^^^^^^

   Build, manage, and share conda, pip, and Docker environments. Use them
   locally or in the cloud.

   +++

   .. link-button:: software_environment
      :type: ref
      :text: Learn more
      :classes: btn-full btn-block stretched-link

   ---

   Manage Teams & Costs
   ^^^^^^^^^^^^^^^^^^^^

   Manage teams, collaborate, set resource limits, and track costs.

   +++

   .. link-button:: teams
      :type: ref
      :text: Learn more
      :classes: btn-full btn-block stretched-link


How Coiled works
----------------

Coiled handles the creation and management of Dask clusters on cloud computing
environments. This process involves your user environment, Coiled Cloud, and a
cloud computing environment.

.. figure:: images/coiled-architecture.png
   :width: 100%
   :alt: Coiled Architecture

   Coiled Architecture (click image to enlarge)

* **User Environment**

  This is where you use the :doc:`Coiled Python package <getting_started>` along
  with your preferred tools to create Dask clusters and submit Dask
  computations. This could be a Jupyter Notebook on your laptop, a Python script
  on a cloud-hosted VM, or Python code within a task in a workflow management
  system.

* **Coiled Cloud**

  `Coiled Cloud <https://cloud.coiled.io/>`_ provides a cluster dashboard that
  you can use to manage clusters, users, teams, software environments, etc.
  Coiled Cloud also handles provisioning the necessary cloud infrastructure for
  your Dask clusters so you don't have to!

* **Cloud Computing Environment**

  This is the cloud environment where Dask clusters will be created and where
  your Dask computations will run. By default, your Dask cluster will be created
  on Coiled’s AWS account. However, you can run Coiled on
  :doc:`different backends <backends>`, including AWS, Azure, or GCP.


Coiled at a glance
------------------

.. tabbed:: Create Dask clusters
   :selected:

   Coiled manages Dask clusters and everything you need to scale Python in the
   cloud robustly and easily. Learn more in the
   :doc:`Dask clusters docs <cluster>`.

   .. code-block:: python

      # Launch a cluster with Coiled
      import coiled

      cluster = coiled.Cluster(
          n_workers=5,
          worker_cpu=4,
          worker_memory="16 GiB",
      )

      # Connect Dask to your cluster
      from dask.distributed import Client

      client = Client(cluster)

.. tabbed:: Use custom software environments

   Coiled helps you manage software environments by building Docker images from
   `pip <https://pip.pypa.io/en/stable/>`_ and
   `conda <https://docs.conda.io/en/latest/>`_ environment files for you. Learn
   more in the :doc:`software environment docs <software_environment>`.

   .. code-block:: python

      # Create a custom "ml-env" software environment
      # with the packages you want
      import coiled

      coiled.create_software_environment(
          name="ml-env",
          conda=["dask", "scikit-learn", "xgboost"],
      )

      # Create a Dask cluster which uses your "ml-env"
      # software environment
      cluster = coiled.Cluster(software="ml-env")



Try Coiled
----------

Ready to get started with Coiled? Sign in and create a free account!

.. link-button:: https://cloud.coiled.io
    :type: url
    :text: Register / sign-in to Coiled
    :classes: btn-full btn-block

Thank you for trying out Coiled!
