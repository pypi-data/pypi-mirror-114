Distributed Properties
======================

The property system allows to expose parameters of pulicast nodes as *Properties*. Those *Properties* can be viewed and changed at runtime by a configurator application by means of *Property Views*.

We now introduce the concepts of a *Property* and a *Property View*.

Properties
----------

The *Property* is owned by a pulicast node.

The owner of a property **must**:

1. initialize the property with some safe default value upon startup.
2. react to requests of change (RoC) to the property.
3. ensure that it acts at all times depending on the value of the property.
4. not (and can not) change the value of a property.

**Initialization:** With a safe default value we mean a value under which the property owner acts in a safe way. For example the default maximum motor speed of a motor controller could be initialized to 0 to prevent any damage. When no safe default can be defined, the value can be set to some None/NaN value. The node must stop acting when not all properties are configured and resume action as soon as all properties are initialized.

**Request of Change:** A node, that receives a RoC to on of its properties, must react to it by either accepting the change and adapting its behavior accordingly or rejecting the change together with a reason why it was rejected. Reasons for rejecting a change could be:

1. a property is constant (for example when it describes a software or hardware version).
2. the requested value is out of feasible bounds (for example the maximum motor speed must be positive).
3. the requested value conflicts with another property's value (for example the maximum motor speed must be larger than the minimum motor speed).
4. the requested value conflicts with the node's internal state (for example the estimators tuning parameters might not be changed mid air but it is OK to change them on the ground).

It is acceptable to modify the value when processing a RoC. For example instead of rejecting a value that is out of bounds, the value can be accepted and then clipped. Such modifications during a RoC should also be accompanied by a reason why the RoC was modified.

**Acting upon properties:** Nodes should transform inputs (subscribed pulicast channels) based on the values of its properties to outputs (published pulicast channels) whenever the necessary preconditions are met. The preconditions might depend on the nodes own internal state, the state of its properties (whether they are configured) and the availability of the inputs, which might be required to arrive at a certain rate or within a certain jitter bound. As long as the preconditions are not met the node stays in an idle state.

Note that the fact whether properties are configured correctly should not be part of the preconditions since the correctness of the configuration should be ensured by rejecting invalid property RoCs in the first place.

**Unchangeable properties:** A node can not change its own properties. The only exception is during a request of change. This is a might seem unintuitive at first, but it is a required technicality to ensure *Property Views* stay in a valid state with regard to the actual property. To export some value/internal state of of a node, an ordinary channel should be used.

Property Views
--------------

The *Property View* lives in a pulicast node, which would usually be distinct from the node owning the property. When it is *in sync*, it knows the value of a property. It can issue requests of change (RoC) after which the view *goes out of sync* until the change is confirmed by the observed *Property*:

(dashed lines are pulicast messages. Normal lines are callbacks)

.. mermaid::

    sequenceDiagram
      participant C as Owner
      participant P as Property
      participant V as PropertyView
      participant S as Observer

      activate P
      activate V
      S ->> V: set [value, timeout, retries]
      V -->>- P: RoC [value]
      Note right of V: view looses sync
      P ->> C: changed [value]
      C ->> P: [value]
      P -->>+ V: [value]
      V ->> S: view synced [retries=0]
      Note over C, S: Setting a property during runtime assuming no lost messages over the (dotted) pulicast transport.
      deactivate V
      deactivate P

The *Property View* sends a request of change to the property which notifies its owning component by callback and sends back the new value as a means of confirmation. When the view receives the confirmation, it becomes synced again and notifies the Observer via a callback. This design only allows for one *Property View* per *Property*!

The case where the property owner rejects a RoC because the property is constant would look like:

.. mermaid::

    sequenceDiagram
      participant C as Owner
      participant P as Property
      participant V as PropertyView
      participant S as Observer

      activate P
      activate V
      S ->> V: set [value, timeout, retries]
      V -->>- P: RoC [value]
      Note right of V: view looses sync
      P ->> C: changed [value]
      C ->> P: [constant value]
      P -->>+ V: [constant value]
      V ->> S: view synced [retries=0]
      Note over C, S: Setting a property during runtime assuming no lost messages over the (dotted) pulicast transport.
      deactivate V
      deactivate P


When messages are lost ...
""""""""""""""""""""""""""

When setting a property using a *Property View*, a timeout and a number of retries need to be specified. If after the timeout no confirmation was received from the Property because of message loss on either way, the change request is sent again until all retries are used up. A special error callback is executed if the value could still not be set.
When all messages are lost:

.. mermaid::

    sequenceDiagram
      participant P as Property
      participant V as PropertyView
      participant S as Observer

      activate P
      activate V
      S ->> V: set [value, timeout, retries=3]
      V --x P: RoC [value]
      deactivate V
      Note right of V: view looses sync
      V ->> V: timeout
      V --x P: RoC [value]
      V ->> V: timeout
      V --x P: RoC [value]
      V ->> V: timeout
      V --x P: RoC [value]
      V ->> V: timeout
      V ->> S: set failed [retries=3]
      Note over P, V: All messages lost
      deactivate P

When only some messages are lost but the set eventually works out, it can happen, that the callback of the owner is triggered more often than necessary. It is therefore important to keep this in mind when implementing the node.

.. mermaid::

    sequenceDiagram
      participant C as Owner
      participant P as Property
      participant V as PropertyView
      participant S as Observer

      activate P
      activate V
      S ->> V: set [value, timeout, retries=3]
      V -->> P: RoC [value]
      Note right of V: view looses sync
      P ->> C: changed [value]
      C ->> P: [value]
      P --x V: [value]
      Note right of V: ack lost
      V ->> V: timeout
      V --x P: RoC [value]
      V ->> V: timeout
      V -->> P: RoC [value]

      P ->> C: changed [value]
      C ->> P: [value]
      P -->>+ V: [value]
      V ->> S: view synced [retries=2]
      Note over P, V: Some messages lost
      deactivate V
      deactivate P


When the Observer restarts ...
""""""""""""""""""""""""""""""

... it will most probably initially override the value of the property so this case is not critical.

When the Owner restarts ...
"""""""""""""""""""""""""""

This is discovered by the node disconnecting. The view becomes invalid and out of sync.

Do we need a "request value" feature?
"""""""""""""""""""""""""""""""""""""

I do not think so. The *Property View* should initially always override the property to ensure it is at a value that it likes.
A "request value" mechanism could be used to obtain the initial value of the property, but it should *by design* not be meaningful for any view. It just should be a safe (as in non-destructive) default. Only constant properties need to be requested and there is already a mechanism for that.

How ROS is doing it
-------------------

https://github.com/ros2/design/blob/4857f0145ab8f743638ebca16f06af3359b4c1ea/articles/055_ros_parameter_design.md

http://wiki.ros.org/sig/NextGenerationROS/Parameters

https://groups.google.com/forum/#!topic/ros-sig-ng-ros/YzCmoIsN0o8

https://github.com/abellagonzalo/dynamic_config
