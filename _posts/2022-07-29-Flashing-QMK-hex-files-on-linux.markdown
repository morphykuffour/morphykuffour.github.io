---
layout: post
title:  "Flashing QMK hex files on Linux"
categories: linux qmk keyboards dfu-programmer 
---

I have been experimenting with custom keyboard layers and keyboards. An annoying difficulty I came across was flashing hex files to my microcontrollers at least on linux OSes. [qmk toolbox](https://github.com/qmk/qmk_toolbox) is a great gui application that makes flashing hex and bin files to microcontrollers a breeze. Unfortunately qmk_toolbox  is only available for Windows and MacOS. The solution I am about to outline should work on most linux distros, I use NixOs btw.

- Search for the dfu-programmer for your distro and install it. On NixOs it's easy as:
```bash
nix-env -iA nixos.dfu-programmer
```

- on ubuntu
```bash
sudo apt-get install dfu-programmer 
```

- Create or get the hex file you want to compile
```bash
cd ~/.qmk_firmware
qmk compile -kb handwired/dactyl_manuform/5x6 -km colemak-dh
ls ./handwired_dactyl_manuform_5x6_colemak-dh
```

- Make sure your microcontroller is connected via usb and verify with `lsusb`
```bash
lsusb
```

- Press the hardware reset button on your microcontroller to put the system into bootloader mode

- Check to see if the device is recognized by dfu-programmer
```bash
# dfu-programmer name_of_board command_to_execute_on_board
 dfu-programmer atmega32u4 get
```
this should output the bootloader version number.

- Erase the current firmware to prep the board for the new firmware you want to flash
```bash
dfu-programmer atmega32u4 erase --force 
```
- Flash the file to the microcontroller board
```bash
dfu-programmer atmega32u4 flash ./handwired_dactyl_manuform_5x6_colemak-dh.hex 
```

- Reset the board ( I honestly do not know why you have type this command but however you cannot start using your keeb unless you type this command or disconnect and reconnect your microcontroller.
```bash
dfu-programmer atmega32u4 reset
```

## resources
```bash
man dfu-programmer
```
See [https://dfu-programmer.github.io/](https://dfu-programmer.github.io/)  
See `SUPPORTED MICROCONTROLLERS` section of the dfu-programmer man page for the supported microcontrollers. 

