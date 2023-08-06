# ZCM to Pulicast Migration Guide

ZCM  |  Pulicast
-----|---------
`#include <zcm/zcm-cpp.hpp>` | `#include <pulicast/pulicast.h>` 
`zcm::ZCM zcm{url}` | `pulicast::AsioNode(node_name, {port})` 
`if(!zcm.good()) {...}` | no need to check. Pulicast always good 
`zcm.subscribe(channel_name, fun)` | `channel.Subscribe<MsgT>(fun)` 
`zcm.publish(channel_name, &msg_object)` | `channel << msg_object`


```c++
void handler(const zcm::ReceiveBuffer* buf, const std::string& channel_name, const MessageType* msg) {}
```
becomes
```c++
void handler(const MessageType& msg) {}
```

## Best Practices

### Pulicast is not thread-safe!

You can still use pulicast in multi-threaded applications with the following hints:

#### Ensure that new channel objects are not created concurrently

Channel objects are created within the node when they are first accessed using `node.GetChannel(name)` or `node[name]`. It is best to just initialize channel references during startup and then pass those channel references to your worker threads. See "Do not store channel names, store channel references" for details.

#### Ensure only one thread is publishing on each channel

I have to dig deeper into the Asio documentation to find out if this measure is sufficient but is necessary for sure. Maybe (if there is a strong need) this restriction will be lifted in the future.

#### Be aware that your callback handlers are called from the Asio event-loop

This means they are called from the thread(s) that execute the `run()` method of the Asio `io_service` object. So you potentially need to introduce locking mechanisms in your handlers (but you had to do that before too).

### Do not write multi-threaded code unless really necessary

Only if you really need more than one CPU core, multiple threads should be used. Maybe also if you need very high timing accuracy another thread is appropriate as well (we still have to figure this out, Asio+multithreading+`asio::strand` something something ...). 

#### Use the AsioTimer to transition from multi-threaded to single-threaded

If you already use the Timer from the ks-timing utils there is good news! There will soon be a replacement called AsioTimer which has mostly the same API but executes the callbacks in the Asio event-loop instead of a new thread. Just switching to this new timer class and abandoning all your thread synchronization primitives might be enough to port your multi-threaded application to a single-threaded application. [See here for an example of how this was archived in the Simulator.](https://code.kiteswarms.com/kiteswarms/simulator/-/merge_requests/70/diffs)

#### Use the AsioTimer multi-threaded

And even more good news: if you decide that you need back multi-threading (for the above mentioned reasons) this is compatible with the AsioTimer as well! We can just call `io_service.run()` from multiple threads and then can use the (much easier to use than locks) `std::strand` mechanism to prevent race conditions.

### Do not store channel names, store channel references

In ZCM we often had code like:

```c++
class MyClass {
//...
    MyClass(zcm::ZCM* zcm, std::string channel_name) 
        : zcm_(zcm), my_channel_name_(channel_name) {}
    void my_method() {
        // ...
        zcm_->publish(my_channel_name_, &msg);
    }
  	zcm::ZCM* zcm_;
  	std::string my_channel_name_;
}
```

Now it is best practice to use channel references instead:

```c++
class MyClass {
//...
    // either
    MyClass(pulicast::Node* node, std::string channel_name) 
        : my_channel_(node->GetChannel(channel_name)) {}
    
    // or
    MyClass(pulicast::Channel& channel) 
        : my_channel_(channel) {}
    
    void my_method() {
        // ...
        my_channel_ << msg;
    }
  	pulicast::Channel& my_channel_;
}
```

### `std::bind` and handler classes are out. Use lambdas for improved readability.

Bind the values that you need inside the lambda. For example `this`:

```c++
// ... somewhere in your constructor ... 
channel.Subscribe<float>(
      [this](const float& msg){
    this->DoSomethingWithFloat(msg);
  });
```

### You want one generic handler for multiple subscriptions and therefore need the channel_name parameter?

Wrap your generic handler in a lambda that bind the channel name like this:

```c++
channel.Subscribe<MessageType>(
    [generic_handler, channel_name=channel.GetName()](const MessageType& msg) {
        generic_handler(channel_name, msg);
    });
```

### Serialization has not changed: we still use ZCM for that