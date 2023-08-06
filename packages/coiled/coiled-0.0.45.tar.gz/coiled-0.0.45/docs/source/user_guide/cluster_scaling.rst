.. _cluster-scaling:

================
Scaling clusters
================

.. currentmodule:: coiled


.. _scaling-clusters:

After you're created a cluster with Coiled, you can scale it up or down using
the :meth:`coiled.Cluster.scale()` functionality. You can input the number of
desired worker nodes to scale up or down to as an integer, as in:

.. code-block:: python

   cluster.scale(20)

For example, to create a cluster with 10 workers and then scale it up to 15
workers, you would run the following commands:

.. code-block:: python

   import coiled

   cluster = coiled.Cluster(n_workers=10)
   cluster.scale(15)

You'll see the new desired cluster size reflected in the Coiled dashboard, and
the new worker nodes will be added and ready to receive work after they are
provisioned and join the Dask cluster.

.. note::

   When scaling a cluster up or down with ``cluster.scale()``, the operation
   will return asynchronously after the scaling request is acknowledged but
   before the desired cluster size is reached.

   If you need to wait for the cluster to reach a specific number of workers
   before continuing, then you can use the
   `client.wait_for_workers() <https://distributed.dask.org/en/latest/api.html#distributed.Client.wait_for_workers>`_
   functionality in the Dask client.

.. important::

   If you're configured Coiled with a backend that
   :doc:`runs on your own cloud account <backends>`, make sure that you've
   requested a sufficient number of instances per your quota/limits to support
   the desired amount of compute resources that you are requesting. Otherwise,
   Coiled will encounter quota limits when requesting additional compute
   resources, and your clusters will not be able to scale up to the desired
   sizes.
