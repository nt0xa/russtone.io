title: 'CheckInstall: Better way to install software compiled from source'
date: 2016-05-27 13:02:24
tags: til, linux
teaser:
	This post describes how to use CheckInstall for install/remove programs
	built from source on Unix-like systems.
---

Often I need to install software that not available in repositories.
The only way to install such software is download its source code, compile it and
install obtained binaries. Usially I do it like this:

``` sh
cd software-source
./configure
make
sudo make install
```

No problems, so far everything seems to be fine.
Problems appear when I want uninstall the software installed in such a way.
Because `make install` can do a lot of things such as copy files, create directories
and symlinks, etc. it can be tricky to find and remove all this things.

The solution I found is to use [CheckInstall](https://en.wikipedia.org/wiki/CheckInstall).
Just install it with:

```sh
# Debian
apt-get istall checkinstall

# Red Hat
yum install checkinstall
```

And instead of `make install` use `checkinstall`:

```sh
cd software-source
./configure
make
sudo checkinstall
```

CheckInstall keeps track of all the files created or modified by an install command and
automatically generate a Slackware-, RPM-, or Debian-compatible package that can
later be cleanly uninstalled through the appropriate package manager:

```sh
# Debian
dpkg -r package-name

# RedHat
rpm -e package-name
```
