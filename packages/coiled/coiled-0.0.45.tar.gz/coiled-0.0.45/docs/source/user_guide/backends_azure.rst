Azure Backend
=============

You can have Coiled launch computations on Azure. Your computations will run
inside Coiled's Azure account, this makes it easy for you to get started
quickly, without needing to set up any additional infrastructure.

.. figure:: images/backend-coiled-azure-vm.png

.. note::

   Azure support is currently experimental with new features under active
   development.

.. tip::

    In addition to the usual cluster logs, our current Azure support also
    includes system-level logs. This provides rich insight into any potential
    issues while Azure support is still experimental.


Switching Coiled to run on Azure
--------------------------------

To use Coiled on Azure select "Azure" in the "Cloud Backend Options" section of
the Account page of your Coiled account.


Region
------

Azure support is currently only available in the ``East US`` region. If you have
data in a different region on Azure, you may be charged transfer fees.


GPU support
-----------

This backend allows you to run computations with GPU-enabled machines if your
account has access to GPUs. See the :doc:`GPU best practices <gpu>`
documentation for more information on using GPUs with this backend.

Workers currently have access to a single GPU, if you try to create a cluster
with more than one GPU, the cluster will not start, and an error will be
returned to you.
