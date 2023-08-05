pyprofibus - PROFIBUS-DP stack
==============================

<https://bues.ch/a/profibus>

pyprofibus is an Open Source
[PROFIBUS-DP](https://en.wikipedia.org/wiki/Profibus) stack written in
Python.

Hardware
========

pyprofibus is able to run on any machine that supports Python. It also
runs on embedded machines such as the [Raspberry
Pi](https://en.wikipedia.org/wiki/Raspberry_Pi) or even tiny
microcontrollers such as the
[ESP32](https://en.wikipedia.org/wiki/ESP32) (Micropython).

Please read the hardware documentation for more information:

[pyprofibus hardware documentation](doc/hardware.html)

Speed / Baud rate
=================

The achievable Profibus-DP speed depends on the hardware that it runs on
and what kind of serial transceiver is used. There is no software side
artificial limit.

Please see the [pyprofibus hardware documentation](doc/hardware.html)

Examples
========

pyprofibus comes with a couple of examples that can teach you how to use
pyprofibus in your project.

-   

    Example that runs pyprofibus without any hardware. This example can be used to play around with pyprofibus.

    :   -   example\_dummy.py
        -   example\_dummy.conf

-   

    Example that runs pyprofibus as master connected to an ET200S as slave.

    :   -   example\_et200s.py
        -   example\_et200s.conf

-   

    Example that runs pyprofibus as master connected to an S7-315-2DP as *slave*.

    :   -   example\_s7-315-2dp.py
        -   example\_s7-315-2dp.conf

Dependencies
============

-   [Python](https://www.python.org/) 3.4 or later.
-   Or alternatively [Micropython](https://micropython.org/). Please see
    the [pyprofibus Micropython help](micropython/README.html) for more
    information.

License
=======

Copyright (c) 2013-2021 Michael Buesch \<<m@bues.ch>\>

Licensed under the terms of the GNU General Public License version 2, or
(at your option) any later version.
