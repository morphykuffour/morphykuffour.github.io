---
layout: post
title:  "learning steno: part 0"
categories: linux i3 keyboard qmk firmware
---

## learning steno

I have been exploring the deepest ends of typing, ergonomics, and stenography recently. I thought about building a georgi keyboard but lack of scad files, time, and my busy school schedule made that idea a mote point. I decided to pickup an off the shelf steno machine, the [uni v4](https://stenokeyboards.com/products/the-uni-v4), since it was cost and time efficient.

Now the biggest challenge is learn the layout of the uni and put in the practice hours to reap the life long rewards of typing close to the speed of my thoughts. To use the uni you have to install plover, an open source stenotype engine that translates mechanical keyboards presses to words with little to no latency. The instructions and [documentation](https://docs.stenokeyboards.com/) provided for the uni is great.

I find it very easy to learn new skills by creating a productive environment that facilitates the learning this new skill. Linux makes it very easy to customize desktop environment to ease the learn process.

I simply wanted to have a floating image of the uni steno layout, something like this: ![floating overlay](/home/morp/Dropbox/screenshots/2022-10-01_04-33.png). 

These are the following pieces of software and hacks I used to make this happen:

* i3wm, a tiling window manager
* kitty, a graphical terminal 
* nixos, a text based linux distro
* community forum answers: https://unix.stackexchange.com/a/474300 

i3, needs handles the keybinding to execute the process and floats the window. Kitty creates a bash process that fork

The following was added to my [https://github.com/morphykuffour/nix/blob/main/modules/i3.nix](i3.nix) to enable i3 to bind the `floatimage` script to `Alt+Shift+M`,
```nix
"${mod}+Shift+m" = "exec kitty --title floatimage_window ${local_bin}/floatimage";
```

The following snippet was also added to my [https://github.com/morphykuffour/nix/blob/main/modules/i3.nix](i3.nix) configuration file to float the window created,
```
for_window [ title="floatimage_window" ] floating enable resize set 640 480
title_align center
```

I then created the script:
```bash
#!/bin/sh

# TODO make image dmenu selectable
imageFilename="$HOME/Dropbox/learn/stenography/uni-layout.png"

if [ ! -f $noteFilename ]; then
  echo "File $imageFilename is not there, aborting."
  exit
fi

kitty +kitten icat $imageFilename &
# sxiv $imageFilename &
pid="$!"

# Wait for the window to open and grab its window ID
winid=''
while : ; do
    winid="`wmctrl -lp | awk -vpid=$pid '$3==pid {print $1; exit}'`"
    [[ -z "${winid}" ]] || break
done

# Focus the window we found
wmctrl -ia "${winid}"

# Make it float
i3-msg floating enable > /dev/null;

# Move it to the center for good measure
i3-msg move position center > /dev/null;

# Wait for the application to quit
wait "${pid}";
```

I put this `chmod`ed the script and put it in my PATH so that my shell could find it.

## nota bene
[floatimage script](https://raw.githubusercontent.com/morphykuffour/dotfiles/main/scripts/.local/bin/floatimage)







