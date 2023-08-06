Amplitude Python SDK
--------------------

SDK for Amplitude API

    | SDK for Amplitude API.
    | https://developers.amplitude.com/docs
    | https://github.com/paulokuong/amplitude

Requirements
------------

-  Python 3.7.0

Goal
----

| To provide a python API client for Amplitude API.
| (More clients to be implemented)

Code sample
-----------

| Requesting Behavioral Cohorts API

.. code:: python

  from amplitude_sdk import BehavioralCohortsClient
  b = BehavioralCohortsClient(
  api_key='xxxxxxx',
  secret='yyyyyyyy')
  b.list_cohorts()


Contributors
------------

-  Paulo Kuong (`@paulokuong`)

.. @pkuong: https://github.com/paulokuong
