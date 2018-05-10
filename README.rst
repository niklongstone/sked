
Sked CLI
========

Configures `AWS Scheduled Scaling`_ for Amazon EC2 Auto Scaling based on Tags.

You can Tag your EC2 instances and define in a config file the scaling profiles. The rest is magic...

.. _AWS Scheduled Scaling: https://docs.aws.amazon.com/autoscaling/ec2/userguide/schedule_time.html

Installation
------------
``$ pip install sked``

Usage
-------
::

  sked create [-c=<config_file>]
  sked delete [-c=<config_file>]
  sked -h | --help
  sked --version


Examples
--------
::

  sked create -c my_schedule.yml
  sked delete -c my_schedule.yml


**If you omit the -c parameter, the cli by default tries to use a file called sked.yml.**

Configuration file sample
-------------------------

::

    # sked.yml
    profiles:
      small:
        desired_capacity: 5
        min_size: 1
        max_size: 10
        recurrence: 0 7 * * * # every day at 07:00
      overnight:
        desired_capacity: 0
        min_size: 0
        recurrence: 15 19 * * MON-FRI # 19:15 from Monday to Friday

    auto_scaling_groups:
      - filter:
          tag:
            key: Name
            value: SomeTag
        schedule:
          - profile: small
            times:
              - start_time: 2018-03-01T00:00:00Z
              - start_time: 2018-04-01T00:00:00Z
      - filter:
          tags:
            - tag: {key: Name, value: MyInstanceA}
            - tag: {key: Name, value: 'My Instance B'}
        schedule:
          - profile: small
            times:
              - start_time: 2018-03-01T00:00:00Z
              - start_time: 2018-04-01T00:00:00Z

Additional Note
---------------

Sked doesn't store the state of the applied scheduled action. Everything is based upon the Yaml configuration file.

If you want to use the delete command make sure you didn't change the Yaml configuration file in the meantime.

For instance, the following workflow **will produce an error**:

1. run ``sked create``
2. change the ``sked.yml`` file
3. run ``sked delete``
