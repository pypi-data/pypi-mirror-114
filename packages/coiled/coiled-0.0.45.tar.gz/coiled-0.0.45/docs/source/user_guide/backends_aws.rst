AWS Backend
===========

Using Coiled's AWS account
--------------------------

When you sign up for a Coiled Cloud account, your Dask clusters and computations
will run within Coiled's AWS account by default. This makes it easy for you to
get started quickly without having to set up any additional infrastructure or
AWS credentials.

.. figure:: images/backend-coiled-aws-vm.png
   :width: 100%

If you configured a different cloud backend option in your account at some
point, you can return to the default mode of running on Coiled's AWS account by
clicking on ``Account`` on the left navigation bar, then clicking on
``Reset to Default``.

.. figure:: images/cloud-backend-reset.png
   :width: 100%


Using your own AWS account
--------------------------

Alternatively, you can configure Coiled to create Dask clusters and run
computations entirely within your own AWS account. This allows you to make use
of security/data access controls, compliance standards, and promotional credits
that you already have in place within your AWS account.

.. figure:: images/backend-external-aws-vm.png
   :width: 100%

Note that when running Coiled on your AWS account, Coiled Cloud is only
responsible for provisioning cloud resources for Dask clusters that you create.
Once a Dask cluster is created, all computations, data transfer, and Dask
client-to-scheduler communication occurs entirely within your AWS account.

Step 1: Obtain AWS credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Coiled provisions resources on your AWS account through the use of AWS security
credentials.

From your AWS Console, create a new (or select an existing) IAM user that will
be used with Coiled.

Once you have created or identified an IAM user for working with Coiled, you'll
need to create new (or use existing) AWS access keys. Follow the steps in the
`AWS documentation on programmatic access <https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys>`_
to obtain your access key ID and secret access key, which will be similar to the
following:

.. code-block:: text

   Example AWS Secret Access ID: AKIAIOSFODNN7EXAMPLE
   Example AWS Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

Keep your security credentials handy since you'll configure them in Coiled Cloud
in a later step.

.. note::

    The AWS credentials you supply must be long-lived (not temporary) tokens.


Step 2: Configure AWS IAM policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Coiled requires a limited set of IAM permissions to be able to provision
infrastructure and compute resources in your AWS account.

From your AWS Console, create a new IAM policy by following the steps in the
`AWS documentation on creating policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-console.html#access_policies_create-json-editor>`_.
Specify an IAM policy name such as ``Coiled`` that will make it easy to locate
in the next step.

When you arrive at the step to insert a JSON policy document, you can copy/paste
the following JSON policy document that contains all of the permissions that
Coiled requires to be able to create and manage Dask clusters in your AWS
account:

.. dropdown:: AWS IAM policy document (JSON)
  :title: bg-white

  .. code-block:: json

        {
          "Statement": [
            {
              "Sid": "Setup",
              "Effect": "Allow",
              "Resource": "*",
              "Action": [
                "ec2:AllocateAddress",
                "ec2:AssociateRouteTable",
                "ec2:AttachInternetGateway",
                "ec2:CreateInternetGateway",
                "ec2:CreateNatGateway",
                "ec2:CreateRoute",
                "ec2:CreateRouteTable",
                "ec2:CreateSubnet",
                "ec2:CreateVpc",
                "ec2:CreateVpcPeeringConnection",
                "ec2:DeleteInternetGateway",
                "ec2:DeleteNatGateway",
                "ec2:DeleteRoute",
                "ec2:DeleteRouteTable",
                "ec2:DeleteSubnet",
                "ec2:DeleteVpc",
                "ec2:DeleteVpcPeeringConnection",
                "ec2:DescribeAddresses",
                "ec2:DescribeInternetGateways",
                "ec2:DetachInternetGateway",
                "ec2:DisassociateAddress",
                "ec2:DisassociateRouteTable",
                "ec2:GetConsoleOutput",
                "ec2:ModifySubnetAttribute",
                "ec2:ModifyVpcAttribute",
                "ec2:ReleaseAddress",
                "ecs:CreateCluster",
                "iam:AddRoleToInstanceProfile",
                "iam:AttachRolePolicy",
                "iam:CreateRole",
                "iam:CreatePolicy",
                "iam:CreateInstanceProfile",
                "iam:DeleteRole",
                "iam:GetInstanceProfile",
                "iam:ListPolicies",
                "iam:ListInstanceProfiles",
                "iam:ListAttachedRolePolicies",
                "iam:TagInstanceProfile",
                "iam:TagPolicy",
                "iam:TagRole",
                "secretsmanager:CreateSecret",
                "secretsmanager:DeleteSecret",
                "secretsmanager:DescribeSecret",
                "secretsmanager:GetSecretValue",
                "secretsmanager:TagResource"
              ]
            },
            {
              "Sid": "Ongoing",
              "Effect": "Allow",
              "Resource": "*",
              "Action": [
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:CreateImage",
                "ec2:CreateSecurityGroup",
                "ec2:CreateTags",
                "ec2:DeleteSecurityGroup",
                "ec2:DescribeAvailabilityZones",
                "ec2:DescribeConversionTasks",
                "ec2:DescribeImages",
                "ec2:DescribeInstanceTypes",
                "ec2:DescribeInstances",
                "ec2:DescribeKeyPairs",
                "ec2:DescribeNatGateways",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeRegions",
                "ec2:DescribeRouteTables",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeVpcPeeringConnections",
                "ec2:DescribeVpcs",
                "ec2:ImportKeyPair",
                "ec2:RunInstances",
                "ec2:TerminateInstances",
                "ecr:BatchCheckLayerAvailability",
                "ecr:BatchGetImage",
                "ecr:CompleteLayerUpload",
                "ecr:CreateRepository",
                "ecr:DescribeImages",
                "ecr:DescribeRepositories",
                "ecr:GetAuthorizationToken",
                "ecr:GetDownloadUrlForLayer",
                "ecr:GetRepositoryPolicy",
                "ecr:InitiateLayerUpload",
                "ecr:ListImages",
                "ecr:PutImage",
                "ecr:UploadLayerPart",
                "ecs:DescribeClusters",
                "ec2:DescribeInstanceTypeOfferings",
                "ecs:DescribeTaskDefinition",
                "ecs:DescribeTasks",
                "ecs:ListClusters",
                "ecs:ListTaskDefinitions",
                "ecs:ListTasks",
                "ecs:RegisterTaskDefinition",
                "ecs:RunTask",
                "ecs:StopTask",
                "iam:CreatePolicy",
                "iam:CreateServiceLinkedRole",
                "iam:GetRole",
                "iam:ListPolicies",
                "iam:ListInstanceProfiles",
                "iam:ListAttachedRolePolicies",
                "iam:PassRole",
                "iam:TagRole",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:GetLogEvents",
                "logs:PutLogEvents",
                "logs:PutRetentionPolicy",
                "secretsmanager:CreateSecret",
                "secretsmanager:DeleteSecret",
                "secretsmanager:DescribeSecret",
                "secretsmanager:GetSecretValue",
                "secretsmanager:TagResource",
                "sts:GetCallerIdentity"
              ]
            }
          ],
          "Version": "2012-10-17"
        }


Step 3: Attach AWS IAM policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you've created an IAM policy to use with Coiled, attach the IAM policy to a
user, group, or role in your account by following the steps in the
`AWS documentation on adding IAM identity permissions <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html#add-policies-console>`__.

However you choose to attach the IAM policy to a user, group, or role - be sure
to verify that that the AWS credentials that you configured earlier are attached
to your new IAM policy that will be used with Coiled.


Step 4: Configure Coiled Cloud backend
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now you're ready to configure the cloud backend in your Coiled Cloud account to
use your AWS account and AWS credentials.

To configure Coiled to use your AWS account, log in to your Coiled account and
access your dashboard. Click on ``Account`` on the left navigation bar, then
click the ``Edit`` button to configure your Cloud Backend Options:

.. figure:: images/cloud-backend-options.png
   :width: 100%

.. note::

   You can configure a different cloud backend for each Coiled account (i.e.,
   your personal/default account or your :doc:`Team account <teams>`). Be sure
   that you're configuring the correct account by switching accounts at the top
   of the left navigation bar in your Coiled dashboard if needed.

On the ``Select Your Cloud Provider`` step, select the ``AWS`` option, then
click the ``Next`` button:

.. figure:: images/cloud-backend-provider.png
   :width: 100%

On the ``Configure AWS`` step, select the AWS region that you want to use by
default (i.e., when a region is not specified in the Coiled Python client),
choose the ``Launch in my AWS account`` option, input your ``AWS Access Key ID``
and ``AWS Secret Access Key`` from the earlier step, then click the ``Next``
button:

.. figure:: images/cloud-backend-credentials.png
   :width: 100%

On the ``Container Registry`` step, select whether you want to store Coiled
software environments in Amazon ECR or Docker Hub based on your preference, then
click the ``Next`` button:

.. figure:: images/cloud-backend-registry.png
   :width: 100%

Review the cloud backend provider options that you've configured, then click
the ``Submit`` button:

.. figure:: images/cloud-backend-review.png
   :width: 100%

Coiled is now configured to use your AWS account!

From now on, when you create Coiled clusters, they will be provisioned in your
AWS account.


Step 5: Create a Coiled cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that you've configured Coiled to use your AWS account, you can create a
cluster to verify that everything works as expected.

To create a Coiled cluster, follow the steps listed in the quick start on your
Coiled dashboard, or follow the steps listed in the
:doc:`Getting Started <getting_started>` documentation, both of which will walk
you through installing the Coiled Python client and logging in, then running a
command such as:

.. code-block:: python

   import coiled

   cluster = coiled.Cluster(n_workers=1)

   from dask.distributed import Client

   client = Client(cluster)
   print("Dashboard:", client.dashboard_link)

.. note::

  If you're using a :doc:`Team account <teams>` in Coiled, be sure to specify
  the ``account=`` option when creating a cluster, as in:

  .. code-block:: python

     cluster = coiled.Cluster(n_workers=1, account="my-team-account-name")

  Otherwise, the cluster will be created in your personal/default account in
  Coiled, which you can access by switching accounts at the top of the left
  navigation bar in your Coiled dashboard.

.. note::

  When you launch your first cluster in your AWS account, Coiled will provision
  the necessary resources. This initial process can take up to 20 minutes. After
  all of the necessary resources are provisioned the first time, subsequent
  clusters will be created much faster - typically in less than 5 minutes.

Once your Coiled cluster is up and running, you can run a sample calculation on
your cluster to verify that it's functioning as expected, such as:

.. code-block:: python

   df = dd.read_csv(
       "s3://nyc-tlc/trip data/yellow_tripdata_2019-*.csv",
       dtype={
           "payment_type": "UInt8",
           "VendorID": "UInt8",
           "passenger_count": "UInt8",
           "RatecodeID": "UInt8",
       },
       storage_options={"anon": True},
       blocksize="16 MiB",
   ).persist()

   df.groupby("passenger_count").tip_amount.mean().compute()

At this point, Coiled will have created a new VPC, subnets, AMI, EC2 instances,
and other resources on your AWS account that are used to power your Dask
clusters. A more detailed description of those AWS resources is provided in the
next section.

.. warning::

  If you are trying to read from an S3 bucket and are getting permissions error
  you might need to attach S3 policies to the role that Coiled creates to be
  attached to EC2 instances.

  The role name that Coiled creates is the same as your account slug.


AWS resources
-------------

When you create a Dask cluster with Coiled on your own AWS account, Coiled will
provision the following resources on your AWS account:

.. figure:: images/backend-coiled-aws-architecture.png
   :width: 90%

   AWS resources for a Dask cluster with 4 workers

When you create additional Dask clusters with Coiled, then another scheduler VM
and additional worker VMs will be provisioned within the same public and private
subnets, respectively. As you create additional Dask clusters, Coiled will reuse
and share the existing VPC and other existing network resources that were
initially created.

.. seealso::

  If you encounter any issues when setting up resources, you can use the method
  :meth:`coiled.get_notifications` to have more visibility into this process.
  You might also be interested in reading our
  :doc:`Troubleshooting guide <troubleshooting/visibility_resource_creation>`.

.. seealso::

  You might be interested in reading the tutorial on
  :doc:`How to limit Coiled's access to your AWS resources <tutorials/aws_permissions>`.

  You might be interested in reading the tutorial on
  :doc:`Managing resources created by Coiled <tutorials/resources_created_by_coiled>`.

Backend options
---------------

There are several AWS-specific options that you can specify (listed below) to
customize Coiled's behavior. Additionally, the next section contains an example
of how to configure these options in practice.

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Name
     - Description
     - Default
   * - ``region``
     - AWS region to create resources in
     - ``us-east-1``
   * - ``spot``
     - Whether or not to use spot instances for cluster workers
     - ``True``

The currently supported AWS regions are:

* ``us-east-1``
* ``us-east-2``
* ``us-west-1``
* ``us-west-2``
* ``ap-southeast-1``
* ``ca-central-1``
* ``ap-northeast-1``
* ``ap-northeast-2``
* ``ap-south-1``
* ``ap-southeast-1``
* ``ap-southeast-2``
* ``eu-central-1``
* ``eu-north-1``
* ``eu-west-1``
* ``eu-west-2``
* ``eu-west-3``
* ``sa-east-1``

.. note::

  Coiled will choose the ``us-east-1`` region by default if you don't
  wish to use this region, you should provide a different region.

.. _backend_options_example:

Example
^^^^^^^

You can specify backend options directly in Python:

.. code-block::

    import coiled

    cluster = coiled.Cluster(backend_options={"region": "us-west-1"})

Or save them to your :ref:`Coiled configuration file <configuration>`:

.. code-block:: yaml

    # ~/.config/dask/coiled.yaml

    coiled:
      backend-options:
        region: us-west-1

to have them used as the default value for the ``backend_options=`` keyword:

.. code-block::

    import coiled

    cluster = coiled.Cluster()


GPU support
-----------

This backend allows you to run computations with GPU-enabled machines if your
account has access to GPUs. See the :doc:`GPU best practices <gpu>`
documentation for more information on using GPUs with this backend.

Workers currently have access to a single GPU, if you try to create a cluster
with more than one GPU, the cluster will not start, and an error will be
returned.
