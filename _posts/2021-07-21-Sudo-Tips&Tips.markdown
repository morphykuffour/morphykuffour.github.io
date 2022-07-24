---
layout: post
title:  "Shell Tips & Tricks"
date:   2021-07-21 14:23:25 -0400
categories: linux
---
Make Sudo suckless.

```bash
# This one-liner will allow you to bypass inputting 
# user defined password everything time you call sudo.
echo "%${USER} ALL=(ALL) NOPASSWD:ALL" | sudo EDITOR='tee ' visudo --quiet --file=/etc/sudoers.d/passwordless-sudo
```

Print exit code of previously excuted commands
```bash
echo "yes"
echo $? 
```
should print 0 if `echo "yes"` was successfully excuted otherwise 1.

Less retyping
```bash
 # run whichever-command on the last argument of the previous command

whichever-command !$     

# For example
ls averylongnameIdonotwantoretype.c   # oops meant to type cat

cat !$                                #cat !$ := cat averylongnameIdonotwantoretype.c 


# Caveat being that "!$" evaluates to the last string 
# passed as an argument to the command in your history. 
# "!$" does not evaluate to all the strings following your previous command.

# For example if I repeated the above mistake again with 2 files now 
ls averylongnameIdonotwantoretype.c test.c             # oops meant to type cat
cat !$                                                 # cat !$ := cat test.c 

# This of course works with any shell command line utility

# Other Shell Tricks

# Let's say I compile and link a cpp program using the following command
g++ -ggdb -O2 -ulimit -Wall -Wno-unused-result -std=c++11 program.c -o program

# I continue working on the program, I step into gdb, and I do other important things.
# Now when I come back to my shell I don't want to retype the long compilation line 
# again so I simply type, 
!g++


# The classic "!!"
# !! expands out to the previous command you passed to your shell
echo $PATH                      # this is equivalent to !-3
ls /proc/$(pgrep -f -n bash)    # this is equivalent to !-2
echo $SHELL                     # this is equivalent to !-1 or !!
!!                              # this is equivalent to "echo $SHELL"
sudo !!                         # this is equivalent to "sudo echo $SHELL"

# Now let's say I want to run sudo on the ls command above 
sudo !-2                        # notice how this just evaluates to echo $SHELL 
                                # not what I wanted
# What I really wanted 
sudo !ls

sudo ls /proc/$(pgrep -f -n bash)   # My current line in the history lists
^bash^tmux^                    # This evaluates previous line substituting bash for tmux.

# The man page for history calls these clever things Event Designators.
# You can think of the history list as a stack that grows down thus the top of the
# stack is the previous command sent to our shell.  
man history  # Event Designators is under the HISTORY EXPANSION section of the man page.

```