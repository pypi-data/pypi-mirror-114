==============================
How to upload a file to Coiled
==============================

When you launch a Cluster to run a computation, you might need to upload
some files to the cluster or perhaps the library requires you to run some
command to download extra files. In this article, we will show you different
ways how you can upload a file to Coiled.

Using the post_build command
----------------------------

When you create a :doc:`software environment <../software_environment_creation>`
you can use the keyword argument ``post_build`` to run a command or adding a path
to a local executable script.

Let's assume that you will use the `spaCy <https://spacy.io/>`_ library in your
computations. You can run the command ``python -m spacy download en_core_web_sm``
to download and install a trained pipeline. You can do this with the ``post_build``
command, for example:

.. code:: python

    import coiled

    coiled.create_software_environment(
        name="spacy",
        conda=["distributed", "dask"],
        pip=["spacy"],
        post_build=["python -m spacy download en_core_web_sm"],
    )

The post build command will run after the conda and pip have installed all
the dependencies.

Using Dask's upload_file command
--------------------------------

Dask allows you to upload a file using the Distributed Client method 
`upload_file <https://distributed.dask.org/en/latest/api.html?highlight=upload_file#distributed.Client.upload_file>`_.
Let's assume that you have a python script that you would like to have 
access while your cluster is running.

.. code:: python

    import coiled
    from dask.distributed import Client

    cluster = coiled.Cluster()
    client = Client(cluster)

    client.upload_file("my_script.py")

As you can see, using the ``upload_file`` allows you to upload a file to a running
cluster, while using the ``post_build`` command can only be used when we rebuild your
software environment.

.. note::

  Using the ``upload_file`` method will also upload the file to all workers.

Creating a docker image
-----------------------

Let's assume that you have many files that you would like to include when using Coiled.
Perhaps it would make sense to build a custom docker image containing all the files you
might need. 

When you build a software environment with Coiled, you can use the keyword argument 
``container=`` to include your custom image.

.. code-block:: python

    import coiled

    coiled.create_software_environment(
        name="custom-container",
        container="user/custom-container:latest",
        conda=["distributed", "dask"],
    )

Note that you can also include dependencies to your docker container so you don't have to
install everything using the ``conda`` or ``pip`` keyword argument.