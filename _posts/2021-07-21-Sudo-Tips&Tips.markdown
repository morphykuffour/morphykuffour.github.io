---
layout: post
title:  "Sudo Tips & Tricks"
date:   2021-07-21 14:23:25 -0400
categories: linux
---
Make Sudo suckless.

```bash
# This one-liner will allow you to bypass inputting user defined password everything time you call sudo.
echo "%${USER} ALL=(ALL) NOPASSWD:ALL" | sudo EDITOR='tee ' visudo --quiet --file=/etc/sudoers.d/passwordless-sudo
```

Less retyping
```bash
 # run whichever-command on the last argument of the previous command

whichever-command !$     

# For example
ls averylongnameIdonotwantoretype.c       # oops meant to type cat

cat !$                                    #cat !$ := cat averylongnameIdonotwantoretype.c 


# Caveat being that "!$" evaluates to the last string passed as an argument to the command in your history. !$ does not evaluate to all the strings following your previous command.

# For example if I repeated the above mistake again with 2 files now 
ls averylongnameIdonotwantoretype.c test.c             # oops meant to type cat
cat !$                                                 # cat !$ := cat test.c 

# This of course works with any shell command line utility

# Other Shell Tricks

# Let's say I compile and link a cpp program using the following command
g++ -ggdb -O2 -ulimit -Wall -Wno-unused-result -std=c++11 program.c -o program

# I continue working on the program, I step into gdb, and I do other important things.
# Now when I come back to my shell I don't want to retype the long compilation line again
# you can simply 
!g++

```