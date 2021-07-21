---
layout: post
title:  "Sudo Tips & Tips"
date:   2021-07-21 14:23:25 -0400
categories: linux
---
Make Sudo suckless.
This one-liner will allow you to bypass input user defined password everything time you call sudo.
```bash
echo "%${USER} ALL=(ALL) NOPASSWD:ALL" | sudo EDITOR='tee ' visudo --quiet --file=/etc/sudoers.d/passwordless-sudo
```