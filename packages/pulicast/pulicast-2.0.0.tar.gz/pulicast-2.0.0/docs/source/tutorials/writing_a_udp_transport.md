# Writing a UDP Transport

When implementing a new UDP transport ...

**Note that:**
1. there is a limit on how many multicast groups can be joined on a single socket.
1. there seems to be a lot of undocumented behaviour in multicast implementations 
   and that the behaviour might differ on different OSes and even switches. 
   Therefore, testing with real hardware is required.

**Ensure that:**
1. the shared `multicast_group_for_channel` function is used to map channel names to multicast groups.
1. the sockets are opened using the flags `AF_INET`, `SOCK_DGRAM`, `IPPROTO_UDP`.
1. there is at most one sending socket per channel.
1. there is a TTL option which is honored.
    * Note: [For some weird reason sending sockets have to join the multicast group on which they send](https://askubuntu.com/a/1243034/1180708).
    Otherwise, the TTL option is not honored and packets with TTl=0 still arrive at foreign hosts.
1. sending sockets should set the IP_MULTICAST_LOOP option to ensure that packets arrive at the loopback device.
1. when TTL = 0, this should imply the network interface is the loopback device or unspecified.
1. there is a way to set the network interface. "0.0.0.0"/Any/None should be valid option which will fall back to an 
   OS-chosen default for sending and receives on any device.
    * Use the IP_MULTICAST_IF option to specify it on sending sockets (if not `Any` interface)
    * For receiving sockets there are two ways to specify it
        * when joining a multicast group, it can be added to the ip_mreq(n).imr_address field (leaving it to 0 amounts to `Any`)
        * by binding the socket to the multicast group (binding to 0 amounts to any address). <- this hack is used by the QT implementation
    * For receiving sockets that join on a non-`Any` interface, 
      it might be necessary to ALSO join on the `loopback` device to ensure that local messages are also received.
      For this the IP_MULTICAST_LOOP option on the sender side MIGHT be enough though (TODO: clarify this)
1. receiving sockets set the SO_REUSEADDR option before binding.
1. receiving sockets set the IP_MULTICAST_ALL option to false/0 to prevent receiving messages,
   that a different process on the same host subscribed.
1. receiving sockets join the corresponding multicast group.
