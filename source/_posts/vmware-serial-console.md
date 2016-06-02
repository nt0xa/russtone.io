title: Control Linux VMware virtual machine over serial port
date: 2016-06-02 15:40:14
category: til
tags: vmware
teaser:
	How to add serial port to your VM, configure it and connect over
	it with PuTTY.
---

It can be useful when you test network communications and you don't want
see SSH traffic in wireshark.

## Add serial port to VM

How to add a serial port to your VM is described in detail in
[this article](https://www.vmware.com/support/ws3/doc/ws32_devices3.html).

## Configure Linux on VM

First, you need to check that you do actually have a serial port:

```sh
user@debian:~$ dmesg | grep tty
[0.000000] console [tty0] enabled
[2.720937] 00:05: ttyS0 at I/O 0x3f8 (irq = 4, base_baud = 115200) is a 16550A
```

So here we have one serial port `ttyS0` with baud rate 115200.

Next, we need to enable getty on this port:

```sh
systemctl enable serial-getty@ttyS0.service
systemctl start serial-getty@ttyS0.service
```

That's all. Now we can try to connect.

## Connect over serial port with PuTTY

Just choose 'Serial', enter port name to 'Serial line' and baud rate to 'Speed':

![](putty.png)
