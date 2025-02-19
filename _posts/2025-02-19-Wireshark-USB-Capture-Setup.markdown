---
layout: post
title:  "Setting up USB capture on Wireshark"
categories: linux Wireshark
---

## Motivation 
I wanted to capture hidapi calls on my ferris sweep in order to debug some code I wrote. I tried following the [Capture Setup](https://wiki.wireshark.org/CaptureSetup/USB) but it did not work. 

## Add default user to wireshark group
The following section is from the wireshark wiki

First, check if you belong to the wireshark group with:

```bash
groups $USER
```


To add yourself to the wireshark group, run the below command, then logout and login.

```bash
sudo adduser $USER wireshark
```

Then ensure that non-superusers are allowed to capture packets in wireshark. Select <Yes> in the below prompt:

```bash
sudo dpkg-reconfigure wireshark-common
```

To dump USB traffic on Linux, you need the usbmon kernel module. If it is not loaded yet, run this command as root:

```bash
sudo modprobe usbmon
```

On most modern Linux systems, **devtmpfs** (which manages `/dev` entries) does not typically support setting ACLs via `setfacl`. That’s why you keep getting errors when trying `setfacl -m u:$USER:r /dev/usbmon*`. Instead, you need to ensure those USB monitor devices have the right group ownership and permissions so that members of the "wireshark" group can access them.

The most reliable way is to use a udev rule:

## Create udev rule

**Create a new udev rule**

For example, create the file `/etc/udev/rules.d/99-usbmon.rules` (the name can vary, but must end in .rules), and add the following line:

```
SUBSYSTEM=="usbmon", MODE="0660", GROUP="wireshark"
```

```bash
echo 'SUBSYSTEM=="usbmon", MODE="0660", GROUP="wireshark"' > /etc/udev/rules.d/99-usbmon.rules
```

This instructs udev to set the device mode to `0660` (read/write for owner and group) and assign the group `wireshark` whenever a `/dev/usbmon*` device is created.

**Reload udev rules and trigger**

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

**Verify permissions**

Check the device permissions:

```bash
ls -l /dev/usbmon*
```

You should now see something like `crw-rw---- 1 root wireshark ... /dev/usbmon0`.

**Ensure you’re in the "wireshark" group**

If you haven’t already:

```bash
sudo usermod -aG wireshark $USER
```

Then log out and log back in (or reboot).

With that setup, Wireshark (or any program run by a user in the "wireshark" group) should be able to open `/dev/usbmon*` without requiring root privileges or ACLs. This is the recommended, standard approach on Debian/Ubuntu systems.

After rebooting you might not see usbmon interfaces in wireshark, simply run the following command

```bash
sudo modprobe usbmon
```

## Resources

[https://wiki.wireshark.org/CaptureSetup/USB](https://wiki.wireshark.org/CaptureSetup/USB)
