.. Pulicast-python documentation master file, created by
   sphinx-quickstart on Tue Apr 14 17:35:58 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pulicast
========
Pulicast is a Publish/Subscribe middleware with UDP as its transport mechanism.
Publishing and subscribing happens on channels which are mapped to `UDP multicast groups <https://en.wikipedia.org/wiki/Multicast>`_.
Messages are serialized using the serializer of `ZCM <https://github.com/ZeroCM/zcm/>`_.

Publishing and subscribing happens via channel objects, which are not directly created, but acquired
from a node object. The node acts as a container for channels that are lazy-created when accessed.

To publish a message do::

   from pulicast import ThreadedNode
   node = SocketNode("test_node")
   node["ping_channel"] << "Hello World"

To subscribe to a channel with a callback do::

  def my_callback(message: str):
      print(message)
  node["ping_channel"].Subscribe(my_callback)
  node.start()


Installation
------------

Install the pulicast library only:

.. code-block:: bash

   $ pip install pulicast

Install the library including tools such as puliconf and puliscope:

.. code-block:: bash

   $ pip install pulicast[tools]

Tutorials
---------

.. toctree::
   :maxdepth: 2

   tutorials/basic_usage
   tutorials/zcm_to_pulicast_migration
   tutorials/writing_a_udp_transport
   .. tutorials/custom_transports
   tools

Concepts
--------

.. toctree::
   :maxdepth: 2

   concepts/ordered_delivery
   concepts/distributed_properties
   concepts/namespaces
   .. concepts/multicast_group_usage
   concepts/threads_and_eventloops



API Reference
-------------

Click `here for the C++ API reference <https://kiteswarms.gitlab.io/pulicast-cpp/>`_.

.. toctree::
   :maxdepth: 2

   pulicast