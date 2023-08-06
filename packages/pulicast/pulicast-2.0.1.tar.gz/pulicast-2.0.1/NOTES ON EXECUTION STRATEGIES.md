# Execution Strategies

There are three main strategies to execute asynchronous code:

## Threads

UDP packets are received and the subscription callbacks are executed in a separate thread/s. In the old pulicast this happens when `pulicast.start()` is called.

## Event Loop

Receiving packets and execution subscription callbacks is managed by an event loop within a single thread. An example would be the Trio event loop or Boost.ASIO. This is not supported by the old pulicast version (except for the implementation for the reference generator).

## Blocking

Packages are received and subscription callbacks are executed from a function called by the pulicast user. This is equivalent to the `pulicast.handle()` and `pulicast.run()` methods in the old pulicast version.

All three execution strategies shall be supported by the new pulicast version because they all have their own justification: 
Threads make use of the full potential multi-core CPUs and do not lock the user into a specific event loop framework. 
Event Loops are useful when the user does not want to deal with the issues of multi-threading as they require less synchronization efforts. They can also be more efficient because there are less context switches. 
The blocking strategy gives the pulicast user full control over the execution of subscription callbacks and are therefore useful in the embedded domain. 

Each execution strategy might require its own implementation of the transport layer and the pulicast handler, while the core of the new pulicast protocol -- message packer and the message dispatcher -- stay the same.