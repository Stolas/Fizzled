
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
Fizzled is a collection of fuzzing scripts. Which most of the time run but not find anything (like all Fuzzing).
Great to run while doing other research.

## Quick start
1. Setup Envoirment / Edit settings.py
2. ~~Run legion, this will fetch samples from the internet.~~
3. ~~Run stalker, find unique attributes in the code.~~
4. Run fizzled in automode.
5. Wait...
6. Read autopsy reports.
7. 0days!


# mutilator.py
Creates files using the configured strategy and stores them in the samples directory.

# taskmaster.py
Picks up a samples from the samples directory.
Moves this to the work directory so other workers can't touch it.
Starts autopsy and moves to crash if autopsy wants this.

# autopsy.py
Autopsy runs the program, and stores the results.

# legion.py
~~Crawls the internet for files and download them to the data directory.~~

Not yet build, for now use:

    find / -type f -iname '*.pdf' -exec cp {} data/ \;

# stalker.py
~~Runs the target file and determines the execution path.~~
~~Stores the fuzzy hash in a file.~~
Not yet build, for now accept that you waste power and CPU Cycles (Maybe use intel pintool for this).

# Logger
All programs use the logger for output, best to set this to a central syslog server.
For this you'll need settings.py, the settings.py is a Django-Style config file.
