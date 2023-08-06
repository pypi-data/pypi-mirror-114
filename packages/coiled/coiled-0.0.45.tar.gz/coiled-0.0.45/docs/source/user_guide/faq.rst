:notoc:

===
FAQ
===

Usage
-----

.. dropdown:: Can I use Coiled to do machine learning, data science, etc.?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes! Coiled builds on the popular PyData ecosystem of tools, and Dask in
    particular. Refer to the following resources to learn more about what you
    can do with Dask and Python:

    -   `Dask <https://dask.org>`_
    -   `Dask Examples <https://examples.dask.org>`_

    You may also want to check out our `YouTube channel
    <https://youtube.com/c/Coiled>`_ for interviews with community members that
    are using Python at scale.


.. dropdown:: Does Coiled support Jupyter notebooks?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes, you can use Coiled from a Jupyter Notebook on your laptop or in a
    cloud-hosted environment.

    Coiled also supports running hosted, sharable notebooks. Click on the
    ``Notebooks`` tab in the Coiled app for example notebooks and steps on how
    to get started. You may also want to try some of our notebooks at
    `cloud.coiled.io/examples/notebooks <https://cloud.coiled.io/examples/notebooks>`_.

    Note that today Coiled does not yet persist user state across notebook
    sessions. Refer to the documentation on :doc:`notebooks` for more
    information.


.. dropdown:: Can I use Coiled from Sagemaker, VS Code, PyCharm, etc.?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes, you can use Coiled from anywhere that you can run Python. Coiled is
    agnostic to any specific user environment, editor, or IDE.


.. dropdown:: Does Coiled support GPUs?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes, however, access to GPU resources is not currently available when using
    the free tier in Coiled Cloud.

    For more information on using GPUs with Coiled Pro, and Coiled Enterprise,
    refer to `coiled.io/pricing <https://coiled.io/pricing>`_ or reach out to us
    at sales@coiled.io.


.. dropdown:: Can I use a container registry other than DockerHub or ECR?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes, a registry that supports the Docker Registry API V2 should work, but it
    is an experimental feature under active development. Please reach out if you
    would like to discuss your use case at support@coiled.io.


Data
----

.. dropdown:: How do I access my data from Coiled?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    When you run computations on Dask clusters managed by Coiled, you can access
    many different file formats using the typical approaches used by Dask,
    Python, and related libraries.

    -   `Tabular data <https://docs.dask.org/en/latest/dataframe-create.html>`_
    -   `Array data <https://docs.dask.org/en/latest/array-creation.html>`_
    -   `Text data <https://docs.dask.org/en/latest/bag-creation.html>`_

    Coiled can provision Dask clusters on different cloud providers. Therefore,
    large datasets should be stored on the cloud using services such as Amazon
    S3 to avoid large data transfer costs. Be sure to also consider which region
    you are running Coiled in compared to which region the data resides in.


.. dropdown:: Do I need to migrate my data to Coiled?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    No, Coiled does not store any of your data. Rather, your data can remain in
    its current location. Coiled manages computation and helps you load data
    from your existing data sources, process it, and write results to those same
    (or other) data sources.


.. dropdown:: Does Coiled collect logs from my Cluster?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    If you are using your AWS credentials, Coiled doesn't collect the scheduler/worker
    logs. Coiled will instead use a token to access the logs in your account to
    show them to you from the cluster dashboard.
    Coiled does have access to server logs which might contain information
    related to your activities.

.. dropdown:: Why does Coiled need ECR permissions?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Coiled stores built software environments as Docker images in ECR based on your
    pip/conda dependencies and use those images when you create a Cluster.
    Even if you don't plan to install any dependencies, Coiled still needs the
    permissions to access your ECR repositories when creating a container only
    software environment.


Libraries
---------


.. dropdown:: How do I install libraries on my Coiled clusters?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Coiled helps you manage software environments both on your local machine and
    on cloud providers. You can specify custom environments using pip or conda
    environment files with the ``coiled.create_software_environment`` function
    and Coiled will manage building Docker images that can then be used as
    software environments in Dask clusters or other jobs on the cloud.

    Refer to the documentation on :doc:`software_environment` for more
    information.

.. _why-local-software:

.. dropdown:: Why do I need a local software environment?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    When performing distributed computations with Dask, you’ll create a
    :class:`distributed.Client` object which connects your local Python process
    (e.g., your laptop) to your remote Dask cluster (e.g., running on AWS). Dask
    ``Client`` s are the user-facing entry point for submitting tasks to a Dask
    cluster. When using a ``Client`` to submit tasks to your cluster, Dask will
    package up and send data, functions, and other Python objects needed for
    your computations *from* your local Python process where your ``Client`` is
    running *to* your remote Dask cluster in order for them to be executed.

    This means that if you want to run a function on your Dask cluster, for
    example NumPy’s :func:`numpy.mean` function, then you must have NumPy
    installed in your local Python process so Dask can send the ``numpy.mean``
    function from your local Dask ``Client`` to the workers in your Dask
    cluster. For this reason, it’s recommended to have the same
    libraries/versions installed on both your local machine and on the remote
    workers in your cluster.

    Refer to the documentation on :doc:`software_environment` for more details
    on how to easily synchronize your local and remote software environments
    using Coiled.


.. dropdown:: Why do I get Version Mismatch warnings?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    When running cloud computations from your local machine, we need to ensure
    some level of consistency between your local and remote environments. For
    example, your Python versions should match, and if you want to use a library
    like PyTorch or Pandas remotely, then you should probably also install it
    locally. When Coiled detects a mismatch, it will inform you with a warning.

    Matching versions can be challenging if handled manually. Fortunately,
    Coiled provides functionality to help build and maintain software
    environments that match across local and remote environments. Refer to the
    documentation on :doc:`software_environment_local` for more information.


Deployment
----------

.. dropdown:: Which cloud providers does Coiled support?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Coiled currently supports running within our managed AWS environment or
    within your own AWS account. Coiled also supports running on our managed
    Azure and GCP environments. Refer to the documentation on :doc:`backends`
    for more information on backend configuration, supported regions, and GPUs.

    Please contact sales@coiled.io if you're interested in using Coiled with
    other backends such as your own Azure account, your own GCP account, or
    Kubernetes.


.. dropdown:: Can Coiled provision resources in my own cloud account?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes! By default, Coiled creates Dask clusters in our managed AWS
    environment. However, for pricing or security reasons you may prefer to have
    Coiled provision compute resources within your own AWS account. Refer to the
    documentation on :doc:`backends` for more information.


.. dropdown:: Can I run Coiled on-premises?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    If you want run Coiled in your own private cloud account, we currently
    support that for AWS. Refer to the question "Can Coiled provision resources
    in my own cloud account?" above.

    If you want to run Coiled on your own machines in your own data center, we
    would love to hear from you. Please contact sales@coiled.io to start a
    conversation with us.


Availability
------------

.. dropdown:: How much does Coiled cost?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    When using the free tier in Coiled Cloud, you will not be charged for any of
    the compute resources you use, however there is a limit of 100 concurrently
    running cores per user and a monthly quota/limit based on usage.

    For more information on pricing, Coiled Pro, and Coiled Enterprise, refer to
    `coiled.io/pricing <https://coiled.io/pricing>`_.


.. dropdown:: How do I invite colleagues, students, etc.?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    We're glad that you're enjoying Coiled and want to invite colleagues or
    students. Coiled is currently open access, so your colleagues can join on
    their own without any additional steps.

    If you want to work within a team account with a group of users from your
    organization, then you can send an e-mail to sales@coiled.io with a team
    name and we'll set you up as an administrator for your new team. Refer to
    the documentation on :doc:`teams` for more information.


Security
--------

.. dropdown:: Can I use Coiled to read private data on AWS?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes. If you create a Coiled cluster from an environment that has AWS
    credentials defined, then Coiled will generate a secure token from those
    credentials and forward it to your Dask workers. The Dask workers will have
    the same rights and permissions that you have by default.

    For additional control, Coiled can be deployed within your own AWS account
    where you can specify and manage IAM roles directly. Refer to the
    documentation on :doc:`security` for more information.


.. dropdown:: Are my computations and data secure?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Coiled provides end-to-end network security by the use of both cloud
    networking policies and with SSL/TLS encryption. Coiled does not persist or
    store any of your data, data only resides in memory as long as you are
    performing computations.

    For additional control, Coiled can be deployed within your own AWS account
    where you can specify and manage data access controls directly. Refer to the
    documentation on :doc:`security` for more information.


Connect with us
---------------

.. dropdown:: How can I submit a bug report, feature request, or other question?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    First, thank you! Your feedback is highly valuable and will help influence
    the future of Coiled.

    For **bug reports**, please :doc:`open a support ticket <support_ticket>`
    and our support team will be happy to help you.

    For **feature requests or other usability feedback**, we'd love to hear from
    you on our :doc:`feedback portal <feedback>`!

    For **other questions**, please join our
    `Coiled Community Slack <https://join.slack.com/t/coiled-users/shared_invite/zt-hx1fnr7k-In~Q8ui3XkQfvQon0yN5WQ>`_
    where you can ask questions and interact with our engineers as well as the
    Coiled community.


.. dropdown:: How can I keep up with the latest news about Coiled?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    To stay up to date with Coiled, you can
    `subscribe to our newsletter <https://coiled.io>`_ and follow us on
    `Twitter <https://twitter.com/coiledhq>`_,
    `YouTube <https://youtube.com/c/Coiled>`_, and
    `LinkedIn <https://www.linkedin.com/company/coiled-computing/>`_.
