Common Pitfalls with Online Applications
========================================

There are command line tools or analysis scripts that serially compute some output from a given input.
Those applications might wait for a file to be loaded from disk, for a network packet or even for user input,
but they never wait for multiple things at once.
They are called **offline** applications.

On the other hand there are servers, GUI applications or control applications,
which all have in common that they observe some input, that trickles in chunk by chunk,
to continuously compute a stream of outputs.
They are event-driven in the sense that they only run to react to some event and do not run top to bottom like most
offline applications.
While an offline application might wait for a network packet to arrive, or for the user to hit enter, such **online**
applications need to wait simultaneously for multiple events.

The fundamental difference between online and offline *applications* stems from the difference between online and offline *algorithms*:

    In computer science, an online algorithm is one that can process its input piece-by-piece in a serial fashion, [...]
    without having the entire input available from the start.

    In contrast, an offline algorithm is given the whole problem data from the beginning [...]
    `(Wikipedia on Online Algorithms) <https://en.wikipedia.org/wiki/Online_algorithm>`_

Also note that

    For many problems, online algorithms cannot match the performance of offline algorithms [and] not every offline algorithm has an efficient online counterpart.
    `(Wikipedia on Online Algorithms) <https://en.wikipedia.org/wiki/Online_algorithm>`_


Since problems are just a lot simpler to solve with offline algorithms, software engineering traditionally was targeted
at offline application development.
This includes programming paradigms, operating systems, libraries and programming languages.

This bias even further increases the gap in difficulty between writing an online and an offline application.
A number of `anti-patterns <https://en.wikipedia.org/wiki/Anti-pattern>`_ quickly emerge when trying to write online
applications with the tools made for offline applications.

Offline Applications
--------------------

While an offline applications has to wait for user input, a file to load from disk or a network packet, its process is paused by the operating system.
Typical examples of Python commands that cause the program to wait would be ``time.sleep()``, ``.read()``
(on opened files), ``print()`` or ``input()``.
Deep down those commands are translated into `system calls <https://en.wikipedia.org/wiki/System_call>`_ which cause
the operating system to pause the process until some input is available or some time has elapsed.

There is no need to wait for more than one event at the same time.
As an example consider the hypothetical implementation of the  ``cat`` command,
which prints out a file and has to wait twice for the operating system.
First to load the file and second to print the file:

.. mermaid::

    sequenceDiagram
        OS ->>+ cat: "args: myfile.txt"
        Note right of cat: parse args
        cat ->>- OS: read "myfile.txt"
        Note left of OS: spinup HD etc.
        OS ->>+ cat: bytes
        Note right of cat: ascii decode bytes
        cat ->>- OS: print ascii
        Note left of OS: put chars to screen
        OS ->>+ cat: done

The corresponding Python code could be::

    import sys
    filename = sys.argv[1]  # parse args
    file_bytes = open(filename, "rb").read()  # read the file
    file_string = file_bytes.decode("ascii")  # ascii decode bytes
    print(file_string)

Notice how the pattern of exchanges between OS and the application is the same for each execution of the program
and it is perfectly mirrored in the source code.

Online Applications
-------------------------

Online applications have an entirely different mode of operation: they are event driven.
After startup they idle and wait for events to be processed.
Each event triggers either a state change, a new event or both.
In a control application, events would usually be messages delivered as network packets or timer expirations,
but in the context of GUI applications, keyboard and mouse inputs as well as OS signals also play a role as events.

For example an estimator might wait for a regularly occurring timer to generate new estimates but it also
waits for network packets consisting of sensor readings:

.. mermaid::

    sequenceDiagram
        par Computing Estimates
            loop every 0.1s
                Timer->>+Estimator: elapsed
                Note left of Estimator: compute estimate
                Estimator->>-Network: send estimate
            end
        and Processing Sensor messages
            loop packets
                Network->>+Estimator: sensor reading
                Note right of Estimator: process sensor
                deactivate Estimator
            end
        end


Anti-Patterns in Online Applications
------------------------------------
The above sequence diagram already hints to the fact, that the estimator is not very well suited to be implemented
in a sequential programming style since there are two tasks to be executed concurrently: estimate generation and sensor
processing.
This is a cause of a number of at least two anti-patterns.


Busy Waiting
^^^^^^^^^^^^

Each of the two tasks can be easily formulated on its own in a sequential programming style:

Estimate generation::

    while True:
        sleep(period)  # blocks
        generate_new_estimate()
        send_estimate()

Sensor message processing::

    while True:
        packet = read_next_network_packet()  # blocks
        if is_sensor_reading(packet):
            process_sensor_reading(packet)

The busy waiting method combines those two tasks by repeatedly checking if one of the tasks needs execution.
Its implementation might look like this::

    next_estimate_time = time.time()

    def estimate_if_due():
        if time.time() > next_estimate_time:
            generate_new_estimate()
            send_estimate()
            next_estimate_time += period

    def process_sensor_reading_if_available():
        if packet_available():
            packet = read_next_network_packet()  # will not block
            if is_sensor_reading(packet):
                process_sensor_reading()

    while True:  # main loop
        estimate_if_due()
        process_sensor_reading_if_available()
        sleep(0.01)
        # sleep is optional but you will add something like this
        # as soon as you realize that busy waiting consumes 100% of your CPU

Busy waiting wastes lots of CPU power with just checking if a new event is ready to be processed.
The call to ``sleep()`` might reduce the CPU load but it makes the timer less accurate and unnecessarily delays message
processing.
It is not just the frequent checking for a new event that wastes CPU cycles, but also the many context switches between
kernel and user-space.

Threading for concurrency
^^^^^^^^^^^^^^^^^^^^^^^^^

At the first glance threading might seem like the solution to the problems caused by busy waiting.
We can just execute the two tasks in two separate threads where it is ok if they use blocking calls::

    def periodically_generate_estimates():
        next_estimate_time = time.time()
        while True:
            sleep(next_estimate_time - time.time())  # blocks the estimate_thread
            generate_new_estimate()
            send_estimate()
            next_estimate_time += period

    estimate_thread = Thread(target=periodically_generate_estimates, daemon=True)
    estimate_thread.start()

    def process_sensor_readings():
        while True:
            packet = read_next_network_packet()  # blocks the sensor_readings_thread
            if is_sensor_reading(packet):
                process_sensor_reading(packet)

    sensor_readings_thread = Thread(target=process_sensor_readings, daemon=True)
    sensor_readings_thread.start()

    estimate_thread.join()
    sensor_readings_thread.join()

This suddenly is much more efficient than the polling method and even seems to properly separate the two tasks from a
software architecture point of view ...

... until you find out that you should not process a sensor reading while computing a new estimate.
The solution to the inefficiency of of busy waiting just introduced another problem called race conditions.
They can be overcome by synchronization techniques such as locks and queues.
In addition to making the code more complex, they also add computational overhead
(threads themselves also cause significant computational overhead depending on the implementation).

The reason why threads are such a trap is that **concurrent computing is easily confused with parallel computing.**

.. note::

    In parallel computing, execution occurs at the same physical instant on separate CPU cores, with the goal of
    speeding up computations.

    By contrast, concurrent computing consists of task lifetimes overlapping, but execution need not to happen at the same
    instant.

Threads are an abstraction designed for parallel computing, but in the above example, they were used for concurrent
computing. Threads happen to degrade to concurrency on single core machines and in Python
(due to the `GIL <https://realpython.com/python-gil/>`_).
In that case they bring all the trouble of computational overhead and required synchronization mechanisms.

That means that in most cases you should only use threads if there are two or more CPU intensive tasks to be executed
concurrently and those tasks do not need to exchange (much) information.
In Python that means the use of the `multiprocessing <https://docs.Python.org/3.6/library/multiprocessing.html>`_
module (otherwise there are no speed gains).

Event-Loops to the rescue
-------------------------

All operating systems offer a method to avoid busy waiting and threads all together.
They have different names such as select, epoll, kqueue but they all provide a way to wait for multiple events at once
and wake up when one of the events was triggered.
Think like ``wait_for_one_of(sleep(period), read_next_network_packet())``.
After wakeup there is an easy way to determine which of the events was triggered (it could be more than one) in order
to process them.

Unfortunately the usage of those mechanisms is still very cumbersome and there are differences between the OS versions.
That is where event-loops come into play.
They wrap the above mentioned system calls and allow to register callbacks for when an event occurred.
Those callbacks are all executed in a single thread, so no synchronization mechanisms are required.
Usually every GUI framework ships with some kind of event-loop such as
`Qt <https://doc.qt.io/qt-5/qeventloop.html#details>`_ and
`GTK <https://developer.gnome.org/gtk3/stable/gtk3-General.html>`_ but there are also more networking focused
event-loops like `Asio <https://think-async.com/Asio/>`_ in C++ and
`asyncio <https://docs.python.org/3/library/asyncio-eventloop.html>`_ as well as
`Trio <https://trio.readthedocs.io/en/stable/>`_ in Python.

Pulicast and Event-Loops
------------------------

Pulicasts uses an event-loop in order to simultaneously wait for multiple network sockets (subscriptions) and to allow
for timed execution of code (just in Python as of now see :meth:`.run_later`) in a single thread.

It supports Trio and Qt in Python and Asio in C++.
For each underlying event-loop there is a different variant of the pulicast node class.
Additionally there is a :class:`.ThreadedNode` implementation that uses threads for concurrency instead of a proper
event-loop.
Note that this threaded node was just implemented for enhanced backwards compatibility with ZCM
and should only be used when a quick and dirty port of an existing ZCM application is required.

The above mentioned :meth:`.run_later` lends itself way to write event driven control applications that do not rely on
a specific node implementation or event loop.
However when events, that are more elaborate than just timeouts, need to be processed such as user input, OS signals
or network traffic from a socket not managed by pulicast, direct access to the event-loops is usually provided.
