# Namespaces

Pulicast channels are arranged in hierarchical namespaces just like files are arranged in a folder hierarchy.
Channels are accessed by relative or absolute path from a given namespace.

When we access the channel `controls` within the namespace `rover1`, we refer to `rover1/controls`.
When the rover has two arms, then the left arms position is most probably found at `rover1/left_arm/pose`, which can
be accessed by `left_arm/pose` from the namespace `rover1`.
When that controller node needs access to the position of its peer for collision avoidance, it can access its channels via `/rover2/pose` or `../rover2/pose` to cross namespace boundaries just like when navigating a 
posix filesystem. A leading `/` accesses the root namespace and `../` traverses up the namespace hierarchy:

Namespace | path | resolved name
----------|------|--------------
rover1/left_arm/ | ctrl | rover1/left_arm/ctrl
rover1/left_arm/ | ../ctrl | rover1/ctrl
rover1/left_arm/ | /ctrl | ctrl
/ | ctrl | ctrl
/ | rover1/ctrl | rover1/ctrl

Note that unlike posix file names, the resolved names do neither contain leading nor trailing slashes.

Since a node is at the same time a namespace, it can be used to access channels.
By default, this represents the root namespace, but it can be changed at construction time to any other namespace:

```python
import pulicast

rover_node = pulicast.Node("rover_controller", default_namespace="rover1", ...)

rover_node["ctrl"] << "Go LEFT!"  # will publish data on rover1/ctrl

arm = rover_node / "left_arm"
arm["ctrl"] << "Twist!"  # will publish data on rover1/left_arm/ctrl

peer = rover_node.make_namespace("rover2")  # note: make_namespace always resolves names from root, not from the nodes namespace!
peer["pose"].subscribe(...)  # will subscribe to rover2/pose
```

## How Namespaces should be used

In short: change your components constructors to accept namespaces instead of node or channel references.

Before the introduction of namespaces it was common to either pass a node, or a channel
to the components of your program if they need to publish or subscribe using pulicast.
Both practices are problematic, for their own reason.

Passing a node to a component means that the component needs to know the full name of the channel it wants to use.
As soon as you want to quickly change the prefix of a channel name 
(for example since you want to run multiple variants of your node), you need to add a mechanism in your components to 
construct those channel names, which adds a lot of unnecessary infrastructure code to your components.

Passing channels to your component lifts the burden of constructing channel names from your components.
However, now all this code to construct channel names clutters your main function where you construct all your 
components. 
Also, the information about the postfix of the channel name is not included in the component anymore, and it therefore
became less self-contained.

Passing namespaces to your components solve this issues.
Now your components can still decide what channel to use within a given namespace and at the same time they can be 
easily relocated to a different namespace.
Since the typical node should only operate in a single namespace, the node itself also represents a namespace, as 
already mentioned above.
This means you can still pass your node to a component.
Just change the constructors of your components to accept namespaces instead of a node or channels.
In Python this is just a matter of convention and type annotations, but in C++ you will actually have to change the 
signatures. 


## How to name your Channels

The channels you use are part of the public API of your node. 
Therefore, their names and namespaces need to be chosen carefully!

When naming channels, try to assume the perspective of whoever will subscribe to the channels you publish or 
whoever will publish to the channels you subscribe.
What should they need to know and what should they not need to know?
They should know *what* information to expect on a channel but neither *where* nor *how* it was computed
since that is an implementation detail that could change at any time.

We list some rules of thumb here, that generally should be followed, unless they should not.
Use your own best judgement on when to introduce exceptions.
Some are already listed.

### The Namespace Hierarchy should reflect the Physical/Logical Structure

When there is a namespace for each physical device, it is easy to spawn multiple instances of a node for each physical 
device in its respective namespace.
Example:
```
├── drivers
│   ├── rover1
│   │   ├── arm
│   │   │   └── attitude
│   │   └── attitude
│   └── rover2
│       ├── arm
│       │   └── attitude
│       └── attitude
└── flyers
    ├── glider1
    │   ├── attitude
    │   └── flap
    │       └── angle
    └── glider2
        ├── attitude
        └── flap
            └── angle
```

### Do not group Channels by Function

For example namespaces like `sensors`, `controllers` or `logging` are not advised.
Two sensors of the same kind or two controllers of the same kind would immediately have colliding channel names this way.

### Do not group Channels by Hardware

Channel names like `groundstation/controller/ctrl`, `axon1/setpoint` or `bno/acceleration` are discouraged.
The hardware on which a controller runs, to which an actuator is attached or that is used to measure acceleration could change at any time.
Also, the exact hardware used should not matter for your peer nodes.  
  
**Exceptions:**
If the information on a channel is related to some specific hardware like the core temperature, CPU load or memory consumption, 
then it is of course advisable to use a channel name that contains a unique identifier for the hardware. 

### Avoid subscribing Channels outside the Default Namespace
The default namespace of a node should be configurable via the command line.
This allows for example to spawn the same controller multiple times for different vehicles just by altering the default namespace. 
When using channels outside the default namespace, this can not be guaranteed.

In general, depending on channels outside the default namespace makes a component less self-contained and more fragile.
It is to be avoided at any costs and exceptions should have a good (documented!) reason or should be only temporary.

**Exceptions:**
When a common logging channel is used by all components, that channel should probably be in the root namespace.

### Do not include *how* information was obtained in the channel name

For example do not name a channel `drone1/ukf_estimate`, name it `drone1/estimate` or `drone1/pose_estimate`.
The `ukf` part of the channel name contains information about how it has been computed which should be of no
concern for any subscribers of the channel. 
It is an implementation detail leaking of the `drone1/ukf` node.

If you want to document, that your estimate comes from a UKF, then name the node running the UKF something like
`pose_ukf`. 
This allows us to see, that some UKF node publishes on `drone1/estimate` in puliscope.

**Exceptions:**
In the unlikely but possible scenario that you want to compare two estimation methods against each other,
publish the different estimates additionally on `drone1/ukf_estimate` and `drone1/ekf_estimate`.

### Do not include the node or component name in the channel

For subscribers, it should generally not matter what node or component produced the information on the channel.
Also, it should at any time be possible to change the node at which some piece of information is computed without having
to change any subscribers.
If, for debugging purposes, it is important to figure out where exactly some data came from the built-in discovery mechanism 
and tools like `puli-sniffer` or `puliscope` can be used.

**Exceptions:**
When you publish information, that is directly related to a node such as logs, when you intend to redirect stdout/stderr
or when you intend to publish some kind of internal state to a channel, then it might make sense to include the node name in the channel name.

### Channels live in Namespaces but Nodes don't

Note that the default namespace of a node does not mean that the node lives *in* that namespace,
and the default namespace will not be prepended to the node name.
The name of a node is mostly arbitrary and only for debugging purposes.
Even duplicate node names are perfectly fine since nodes are disambiguated by a unique session ID.