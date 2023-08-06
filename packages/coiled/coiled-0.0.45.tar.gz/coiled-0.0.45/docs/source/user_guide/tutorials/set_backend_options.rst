======================================
Setting Backend Options via Python API
======================================

This article will show you how you can use the Python API to set backend
options.

Coiled allows users to configure the cloud computing resources they wish
to use (their "backend") via the ``set_backend_options()`` function. This
function returns the current account username when invoked
and controls backend settings via keyword arguments.  Backend options,
when changed via the Python api will be reflected in the Coiled Cloud
UI, and will persist until changed again via the UI or via
``coiled.set_backend_options()``.

Using coiled.set_backend_options
--------------------------------

This function is fully documented in the `API Reference  <https://docs.coiled.io/user_guide/api.html#>`_ section
of the Coiled documentation; this tutorial provides some example usage as a
supplement to that.

Called without arguments, it returns the current username, and will apply
default keyword arguments.

.. code:: python

    import coiled

    coiled.set_backend_options()

In this case, that will set ``backend_type='vm_aws'``, ``registry_type='ecr'``
and ``region='us-east-1'``. It also sets ``registry_uri='docker.io'``, but as
``registry_type='ecr'`` the value for ``registry_uri`` is moot.

Note that these currently differ slightly from the the default Coiled Cloud
backend options when they are configured via the Cloud UI.
(see ``use_coiled_defaults`` below).

To set all backend options to correspond to the Coiled Cloud UI backend defaults,
selecting the AWS ECS backend with ECR registry, use:

.. code:: python

    coiled.set_backend_options(use_coiled_defaults=True)

To specifically set the backend to AWS ECS:

.. code:: python

    coiled.set_backend_options(backend_type="ecs")

Again, note that this will also reset other keyword arguments with defaults,
most notably ``registry_type='ecr'``, so setting ``backend_type="ecs"``  is
functionally equivalent to ``use_coiled_defaults=True``.

To set the backend to the Coiled-hosted AWS VM backend:

.. code:: python

    coiled.set_backend_options(backend_type="vm_aws")

To set the backend to use user-provided credentials in an AWS VM backend:

.. code:: python

    coiled.set_backend_options(
        backend_type="vm_aws",
        aws_access_key_id="#-your-access-key-ID#",
        aws_secret_access_key="######-your-aws-secret-access-key-######",
        create_vpc=True,
    )


Use care with any code including
private credentials in plain text. Note that it is important to include
``create_vpc=True`` as it will otherwise default to ``False``, and
leave the backend within the Coiled-hosted AWS VM account.

To set the backend to use the Coiled-hosted GCP backend:

.. code:: python

    coiled.set_backend_options(backend_type="vm_gcp")


Additional settings
-------------------

Other settings can be changed via ``coiled.set_backend_options``.  For instance,
AWS regions can also be set:

.. code:: python

    coiled.set_backend_options(region="us-west-1")

For a list of supported regions, see the `AWS backend documentation  <https://docs.coiled.io/user_guide/backends_aws.html>`_.

It is also possible to specify a Docker registry for your software
environments. For example, to use Docker Hub:

.. code:: python

    coiled.set_backend_options(
        registry_type="docker_hub",
        registry_uri="docker.io",
        registry_username="your-registry-username",
        registry_access_token="#######-registry-access-token-######",
    )


In using the preceding, keep in mind default Python behavior, which will reset
keyword arguments ``backend_type='vm_aws'``, ``registry_type='ecr'``,
``region='us-east-1'`` and ``registry_uri='docker.io'`` if they are not
explicitly included in the call.  So, if the goal is to use a user specified
Docker Hub container registry while working in GCP, that keyword argument must
also be set:

.. code:: python

    coiled.set_backend_options(
        backend_type="vm_gcp",
        registry_type="docker_hub",
        registry_username="your-registry-username",
        registry_access_token="#######-registry-access-token-######",
    )
