==================================
Launch a cluster from within a job
==================================

This tutorial will show you how you can use Coiled jobs to launch a cluster
and run computations. Jobs are a way to do batch operations, running other
Python applications or running a Python script. You can
:doc:`read more about jobs <../jobs>` in our documentation.


Set up
------

We will use the example on our :doc:`quickstart <../getting_started>` to show
you how you can run a computation with Coiled using the yellow taxi trip
dataset. The job will do the following:

* Create a Coiled cluster
* Read data from a public S3 bucket
* Perform a computation
* Log the results

Creating the software environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's begin by creating the software environment that we will use to run our
job. Note that you need to specify ``coiled`` as a dependency to import it
from the python script that we will create after.

.. code:: python

    coiled.create_software_environment(
        name="job-test", conda={"channels": ["conda-forge"], "dependencies": ["coiled"]}
    )

Creating the script
^^^^^^^^^^^^^^^^^^^

Once the software environment process completes, we can create a new python file
named ``yellow_trip_data.py`` this file will contain our script that will be
called when we start a new job. We will also upload this file when we create
our job configuration on the next step.

.. code:: python

    import dask.dataframe as dd
    from dask.distributed import Client

    import coiled

    if __name__ == "__main__":
        with coiled.Cluster(n_workers=10, software="job-test") as cluster:
            with Client(cluster) as client:
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

                tip_amount_mean = df.groupby("passenger_count").tip_amount.mean().compute()

        print(tip_amount_mean)


Creating the job configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you create a job configuration, you can use the keyword argument ``files``
to specify a list of files you would like to upload. These files can then be
used when you start a job. You can read more about the command
:doc:`create_job_configuration <../jobs>` in our documentation.

.. code:: python

    coiled.create_job_configuration(
        name="cluster-in-job",
        command=["python", "yellow_trip_data.py"],
        software="job-test",
        cpu=2,
        memory="4GiB",
        files=["yellow_trip_data.py"],
    )

Starting the job
^^^^^^^^^^^^^^^^

Jobs are currently experimental with new features under active development.
This is why you can't access the logs with a command from our Python client
yet. We are working hard to improve the jobs experience - you can see the
logs in your AWS account in cloudwatch.

.. code:: python

    coiled.start_job(configuration="cluster-in-job")

The ``start_job`` command will return once ECS has finished providing the
task; this means that the command will return with the job id and nothing
else. If you go to your dashboard at `cloud.coiled.io` you will see that
the cluster will spin up. Once it finishes the computation, it will
automatically stop.

Getting the logs
^^^^^^^^^^^^^^^^

You can get logs from a job with the command ``coiled.job_logs``, you
probably noticed that when you started the job, we return the job id/name. 
You can also get the id/name back with the command ``coiled.list_jobs``.

Since the command ``coiled.job_logs`` return a dictionary, we are going to
use pretty printer to get the logs in a nicer format.

.. code::

    import pprint

    pp = pprint.PrettyPrinter(indent=4)

    logs = coiled.job_logs(name="<your job id here>")

    pp.pprint(logs["Process"])

Important notes
---------------

Since jobs are an experimental feature, you might encounter unexpected
situations that will require you to debug why this situation happened. Remember
that you can get help from our :doc:`support resources <../support>`.

If you are trying to access an S3 bucket, the role that Coiled creates
might not have S3 permissions, even though your user might have. If you
encounter a permissions error, you can attach the S3 permissions to the
role that Coiled created.
