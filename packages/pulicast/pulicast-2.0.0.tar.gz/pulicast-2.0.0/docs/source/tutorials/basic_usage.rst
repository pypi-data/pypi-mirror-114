Basic Usage
===========

In a pulicast network, each process is considered a node and must instantiate one of the pulicast :class:`.Node` objects
such as :class:`.QtNode` or :class:`.SocketNode`
(read :doc:`/concepts/threads_and_eventloops` to understand why multiple different node objects are provided).

The node announces itself in the network and provides access to the pulicast channels::

    node = pulicast.SocketNode("my_node_name")
    node.start()
    channel = node["my_pulicast_channel"]

We can publish messages on a channel which will arrive at all nodes, that subscribed to the channel::

    def message_handler(message: str):
        print("We Received:", message)
    channel.subscribe(message_handler)
    channel << "Hello World"  # Sends a message to the channel

The Node
--------

Each node must have a name to identify it in the pulicast network.
There could be two nodes with the same name, but by convention that should only be the case when the same application is started twice.

In addition to the name, we can specify the port on which the node should join the pulicast network.
Using different ports allows us to operate multiple pulicast networks on the same network infrastructure.
The default port of pulicast is 8765.

The `time-to-live (ttl) <https://en.wikipedia.org/wiki/Time_to_live>`_ parameter specifies for how many hops packages are forwarded.
The default of 0 will only send messages to nodes on the same host to avoid spamming other hosts in the network by accident.

A node announces itself in regular intervals with all its subscriptions and publications.
This enables easier debugging using the puliscope, :doc:`/concepts/distributed_properties` and detection of frozen or disconnected nodes.
The heartbeat period parameter allows to control how frequently the node repeats the announcements.
While a lower heartbeat period minimizes the failure and property detection delay, it incurs performance penalties in
the form of computation time on the side of the node and increased network load.
It is up to the user to find a good trade-off for the specific application.
The default period is 0.1 seconds.

Publishing
----------

Publishing to a channel happens by streaming messages into a channel
(or using the :func:`pulicast.core.channel.Channel.publish_message` function).
Messages can be:

* any ZCM message, that has been registered using ``pulicast.seralization.register_zcm_package`` or ``pulicast.seralization.register_zcm_type``
* any of the primitive types (``int``, ``float``, ``bool``, ``str``) which will then be converted to a ZCM message of appropriate type before sending
* a ``bytes`` array which will be sent directly without further processing or serialization

.. note:: While it might be the most common use case that only one node publishes on a channel,
    any number of nodes might publish on a channel simultaneously.

Subscribing
-----------

Subscribing to a channel means registering a callback (a subscription handler) to be called whenever a new message arrives on a channel.
The callback takes the new message as an argument along with optional arguments describing meta-information about the
message.

If only messages of a certain type are of interest, a type annotation can be added to the message argument::

    def string_message_handler(message: str):
        print(message)

    def any_message_handler(message):
        print(message)

Here, the ``string_message_handler`` will only be called when a string message arrives on the channel, while the
``any_message_handler`` will accept all kinds of messages.
When annotating with the ``bytes`` type, the deserialization can be circumvented and access to the raw message bytes is
provided.
Subscribing to any of the primitive ZCM wrapper types
(named ``pulicast_messages.{int8, int16, int32, int64, string, boolean, byte, double, float}_msg``) such as the ``pulicast_messages.int32_msg``
allows to circumvent the automatic unpacking of those messages to appropriate python types.

In addition to the ``message`` parameter (which can have any name as long as it is the first parameter of the callback),
the parameters ``lead`` (optionally annotated with ``int``) and source (optionally annotated with ``pulicast.SocketID``)
can be added to the callback in order to gain more information about the message.

The lead indicates how much a message is out of order with respect to other messages arriving on the channel.
A value of 1 indicates that the message arrived in order, for the interpretation of other values see :doc:`/concepts/ordered_delivery`.

The source indicates from what IP/port combination the message originates.
This can help to distinguish different publishes on a channel.

.. note:: This port is not the same port as used when setting up the node.
    It is randomly chosen by the operating system when an application starts.

Pulicast allows to finely control in what thread the subscription handlers are executed.
See :doc:`/concepts/threads_and_eventloops` for details.
