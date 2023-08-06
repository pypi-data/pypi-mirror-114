:notoc:

=========
Notebooks
=========

Coiled supports running hosted, sharable notebooks on https://cloud.coiled.io
through the :func:`coiled.create_notebook` interface. This enables you to run
Jupyter sessions on the cloud with no local setup.

.. note::

    Coiled notebooks are currently experimental with new features under active
    development

When creating a Coiled notebook, you can specify:

- Software to install for use in your Jupyter session
- Any hardware resources to specify (e.g. amount of RAM, number of CPUs)
- Local files to upload for use in the notebook (e.g. a local ``.ipynb`` notebook file)
- Description of the notebook which will be rendered on https://cloud.coiled.io

For example, below is a snippet which creates a "xgboost-demo" Coiled notebook:

.. code-block:: python

    import coiled

    coiled.create_notebook(
        name="xgboost-demo",
        conda={"channels": ["conda-forge"], "dependencies": ["xgboost", "dask"]},
        cpu=2,
        memory="8 GiB",
        files=["analysis.ipynb"],
        description="Analyzes dataset with XGBoost",
    )

.. note::

    Currently any directory structure for uploaded ``files`` will be removed and
    files will be placed in the working directory of the Jupyter session. For
    example, ``/path/to/notebook.ipynb`` will appear as ``notebook.ipynb`` in
    the Jupyter session.

After you've created a notebook, you can run the notebook by navigating to the
"Notebooks" tab on the left sidebar of https://cloud.coiled.io. There you'll
find entries for notebooks you've created (see the screenshot below for an
example), each of which has a button to launch a new Jupyter session for the
corresponding notebook.

.. note::

    By default, any Coiled notebooks you create are publicly accessible to other
    Coiled users to promote sharing and collaborating. Private notebooks will be
    added in the future.

.. figure:: images/notebooks.png


Using a custom image
--------------------

By default, the command :func:`coiled.create_notebook` will use the Docker image
``coiled/notebook:latest`` to create your notebook, this image contains all the
necessary dependencies and configuration for you to get started using notebooks.

If you want to use a custom image when creating a notebook, you will need to do
some changes on how you create the notebook.

* Make sure that you have ``jupyterlab`` installed
* Add a custom command to start the notebook

For example, you could create your notebook following this snippet:

.. code-block:: python

    import coiled

    coiled.create_notebook(
        name="my-custom-notebook",
        container="<your custom image>",
        conda=["jupyterlab", "ipywidgets"],
        command=("jupyter", "lab", "--allow-root", "--ip=0.0.0.0", "--no-browser"),
    )

Remember that you can still upload your files using the ``files`` keyword,
alternatively you can copy those files into your custom image and they will be
accessible when you start a notebook.

.. warning::

    Even though you can access your files from your image, you will need to do
    some admin work if you want to save your work, since notebooks might be
    shutdown after some inactivity, making your changes unrecoverable.


Environment Variables
---------------------

If you want to add environment variables to your notebooks, use the ``environ``
keywork argument of ``coiled.create_notebook``. The input of ``environ`` should be
a dictionary.

.. code-block:: python

    import coiled

    coiled.create_notebook(
        name="my-custom-notebook",
        container="<your custom image>",
        conda=["jupyterlab", "ipywidgets"],
        command=("jupyter", "lab", "--allow-root", "--ip=0.0.0.0", "--no-browser"),
        environ={
            "DASK_COILED__ACCOUNT": "alice",
            "DASK_DISTRIBUTED__SCHEDULER__WORK_STEALING": True,
            "DASK_DISTRIBUTED__LOGGING__DISTRIBUTED": "info",
        },
    )

.. warning::

    Environment variables are not encrypted and will be available as plain text.
    For security reasons, you should **not** use environment variables to store secrets
    in your notebooks.

.. warning::

   Environment variables currently do not work with container only notebooks.


Stopping a notebook
-------------------


Coiled hosted notebooks are ephemeral. Once the notebook is shutdown, the work
that you have done will be lost. Please make sure you download the notebook by 
selecting ``File>Download``, if you wish to save a copy of the notebook locally.

.. warning::

    If a hosted notebook is not shut down or stopped, it will use your credits 
    even if you close the tab or the browser.

It's always a good idea to shut down the notebook once you have finished doing some
work on it. You can do this by selecting ``File>Shutdown.``

.. figure:: images/notebook-shutdown.png

If you have forgotten to shut down your notebook and closed the tab in which it was
running. You can stop the notebook job by using the following commands in your ipython 
session (or anywhere you can run Python.

.. code:: python

    import coiled

    coiled.list_jobs()
    # Returns {"yourusername-82u4dh": {...}}

    coiled.stop_job("yourusername-82u4dh")

    coiled.list_jobs()
    # Should return {}

Please refer to the :doc:`jobs` documentation for more information about managing jobs.
