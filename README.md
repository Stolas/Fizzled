
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

## Quick start
1. Run the config tool, answer the questions to configure Fizzled.
2. Run legion, this will fetch samples from the internet.
3. Run stalker, find unique attributes in the code.
4. Run mutilator to create mutations.
5. Run taskmaster.
6. Read autopsy repotrs.
7. 0days!


# mutilator.py
Creates Charlie Miller style random files and stores them in the samples directory.

# taskmaster.py
Picks up a samples from the samples directory.
Moves this to the work directory so other workers can't touch it.
Starts autopsy and moves to crash if autopsy wants this.

# autopsy.py
Autopsy runs the program, and stores the data.

# legion.py
Crawls the internet for files and download them to the data directory.

# stalker.py
Runs the target file and determines the execution path.
Stores the fuzzy hash in a file.

# config,py
Can check if the config is correct, eg directorys exist.
Also provides the other scripts with config loading functions.

# Syslog
All programs use the logger for output, best to set this to syslog.

