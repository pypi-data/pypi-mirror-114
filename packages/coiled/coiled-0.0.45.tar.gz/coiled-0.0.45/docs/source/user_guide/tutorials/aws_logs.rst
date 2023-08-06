==================================
How to find Coiled ECS logs on AWS
==================================

.. note::

    This method only applies to the ECS backend, other backends will
    show the logs in a different tool.

This article will show you how you can find the logs that Coiled creates
when you are running Coiled on your own AWS Account. It's important to
know where these logs are, specially if you want to have access to a job
logs.

AWS Cloudwatch
--------------


When using your own credentials, Coiled will use
`CloudWatch <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html>`_
to store logs from Clusters launched on the ECS backend.

.. figure:: ../images/aws-cloudwatch.png

You can search for CloudWatch on AWS search bar, Coiled will create a folder
with your account name and inside we will store logs from each cluster and job
that you have started. These logs will be stored for 30 days.