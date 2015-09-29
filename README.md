 ______ _         _          _
|  ____(_)       | |        | |
| |__   _ _______| | ___  __| |
|  __| | |_  /_  / |/ _ \/ _` |
| |    | |/ / / /| |  __/ (_| |   +---------------+
|_|    |_/___/___|_|\___|\__,_|   | Worker A      |
                                  +---------------+
                            +-----+ samples/      |
                            |     | work/         |
                            |     | work/crashed/ |
   +---------------+        |     | taskmaster.py |
   |NAS / NFS Share|        |     | autopsy.py    |
   +---------------+        |     |               |
   |data/          |  Mount |     +---------------+
   |samples/       <--------+
   |mutilator.py   |        |     +---------------+
   +------+--------+        |     | Worker B      |
          |                 |     +---------------+
          |                 +-----+ samples/      |
          | Log                   | work/         |
          |                       | work/crashed/ |
   +------v------+       Log      | taskmaster.py |
   |Syslog Server<----------------+ autopsy.py    |
   +-------------+                |               |
                                  +---------------+

# Fizzled
Fizzled is a collection of fuzzing scripts. Which most of the time run but not find anything.

# mutilator.py
Creates Charlie Miller style random files and stores them in the samples directory.

# taskmaster.py
Picks up a samples from the samples directory.
Moves this to the work directory so other workers can't touch it.
Starts autopsy and moves to crash if autopsy wants this.

# Autopsy.py
Autopsy runs the program, and stores the data.

# Syslog
All programs use the logger for output, best to set this to syslog.
