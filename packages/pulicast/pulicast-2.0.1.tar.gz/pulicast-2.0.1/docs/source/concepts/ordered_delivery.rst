Ordered Delivery
================

Since UDP does not guarantee ordered packet delivery, messages can arrive
out of order, go missing or arrive more than once.
While Pulicast does not solve this issue, it provides the ``lead`` parameter to the message
callbacks to help deal with it in the application layer (the code, that *YOU* write).
The lead value indicates how a message arrived out of order.
It denotes the distance to the newest (as in highest sequence number) arrived packet.

* A lead of **1** indicates, that everything is ok and the message arrived in order.
* A lead of **0** indicates that the message arrived twice in a row.
* A lead **>1** indicates that the message arrived too early. We would have expected other
  messages to arrive before. Those other messages might still arrive or they might have been dropped.
* A lead **<0** indicates that a message arrived too late and therefore out of order.
  Newer messages have already arrived and this one is probably outdated by now.

The lead is computed as ``sequence_number - last_sequence_number`` while last sequence number is continuously updated
using ``max(last_sequence_number, sequence_number``.
The lead of the first message is always one since for that message we can not know if it is in order or not.

Note that one last sequence number is maintained `per sender` and `per channel`.
That means that out-of-order messages on one channel do not affect the ordering on another channel and
out-of-order messages from one sender do not affect the ordering of messages from another sender.

Since it is a common use case to be only interested in the newest messages, there is the
:func:`pulicast.core.channel.Channel.subscribe_ordered` function, that behaves just like :func:`pulicast.core.channel.Channel.subscribe`
but skips messages with ``lead < 1``.

In the following example scenario, messages with the sequence numbers 10 to 14 are received.
Each box designates a message with the corresponding sequence number.
The arrows indicate the order in which the messages arrive and the lead of the arriving message.
In the nominal case the lead will always be 1:

.. graphviz:: nominal_message.dot

Out-Of-Order Messages
---------------------
In this example message 12 arrives delayed after message 13.
This means that message 13 arrives with lead 2 to indicate that one previous message has been skipped and
message 12 arrives with a lead of -1 to indicate that it is delayed/outdated.
Note that message number 14 has a lead of 1 and not 2 since the lead is always relative to the highest sequence number,
not relative to the most recently arrived sequence number.

.. graphviz:: out_of_order_message.dot

Duplicate Messages
------------------
When a message arrives two times in succession, the lead is 0 as in this case with the second arrival of message 11.

.. graphviz:: duplicate_message.dot

Note however, that if a message is delayed **and** duplicated,
this can not be detected by just watching out for a lead of 0 as the following example illustrates:

.. graphviz:: undetected_duplicate_message.dot

Lost Messages
-------------
Unfortunately, we can never know if a message is lost or just delayed by a very large amount of steps.
So a lead >1 always indicates that either a message has been lost or a message has been delayed.

.. graphviz:: lost_message.dot
