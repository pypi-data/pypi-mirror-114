==================
Security & Privacy
==================

This page outlines Coiled's security and privacy policies.


Security policies
-----------------

Coiled credentials
^^^^^^^^^^^^^^^^^^

When you :ref:`set up Coiled <coiled-setup>` with the ``coiled login`` command
line utility, your account username and token are stored in a local
configuration file. This username and token combination gives access to run
computations from a Coiled account and should be treated like a password.

Communication
^^^^^^^^^^^^^

Coiled generates TLS certificates on a per-cluster basis which are used to
manage access to each cluster's Dask scheduler and workers. These certificates
are stored encrypted in our database. Additionally, the scheduler and workers
for a cluster use
`secure communication between them <https://distributed.dask.org/en/latest/tls.html>`_
and are isolated by AWS networking security groups.

If a higher level of security is required for your application, please contact
sales@coiled.io to inquire about deploying Coiled on your internal systems.

Run in your infrastructure
^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, Coiled computations are run within our managed cloud environments.
For additional security, you can configure Coiled to deploy compute resources on
infrastructure that you control (e.g., within your own AWS account). In this
configuration, the control plane is still managed by Coiled, but all compute
resources, access to sensitive data, storage of software environment images, and
system logs will happen entirely within your cloud account.

Refer to the :ref:`data handling <data-handling>` and :doc:`backends <backends>`
sections in our documentation for more information.

AWS credentials
^^^^^^^^^^^^^^^

Often Dask workers in a cluster will need AWS permissions to access private data
or private AWS services. To address this need, Coiled will use the AWS
credentials from your account to generate a session token and then forward that
token to the Dask workers in your cluster.

Note that having local AWS credentials is not required to use use Coiled.
However, in this case only publicly accessible data and services will be
available to your cluster.


Privacy policies
----------------

Sharing by default
^^^^^^^^^^^^^^^^^^

Information like your software environments, cluster configurations, and
notebooks are publicly accessible by default to promote sharing and
collaboration. However, you may also create private software environments and
cluster configurations if you prefer. See the
:ref:`software visibility <software-visibility>` and
:ref:`cluster configuration visibility <cluster-config-visibility>` sections for
more information on private software environments and cluster configurations,
respectively.

Note that information about any cluster running on your account is *not*
publicly accessible and is only available to users which are members of the
account.


.. _data-handling:

Data handling
^^^^^^^^^^^^^

Coiled stores basic user data when you create an account, such as your name,
email address, username, and social login. Additionally, Coiled stores metadata
from your Dask clusters such as task counts and memory usage, similar to the
diagnostic information that is displayed in the Dask dashboard.

There are a few different types of metadata that Coiled stores to be able to
create and manage Dask clusters. Depending on the data type, this metadata is
stored in secure systems that are maintained by Coiled. The retention of this
metadata varies depending on the data type and whether it is used on an ongoing
or temporary basis.

The following metadata is stored in an encrypted database and retained on an
ongoing basis until manually deleted:

- Account/team metadata (e.g., username, email address, team accounts quotas)
- Cluster and jobs metadata (e.g., cluster size, task counts, compute time,
  memory usage)
- Software environment metadata (e.g., Docker image URLs, Python package
  dependencies)

The following metadata is stored in an encrypted cloud-logging service and
retained on a temporary basis then removed after 30 days:

- Cluster and jobs metadata (e.g., cluster size, task counts, compute time,
  memory usage)
- Software environment metadata (e.g., Docker image URLs, Python package
  dependencies)

A full description of what information is collected, as well as how we use and
do not use this information, is listed on our
`Privacy Policy <https://coiled.io/privacy>`_.


Reporting
---------

Any security-related concerns can be reported to security@coiled.io.
