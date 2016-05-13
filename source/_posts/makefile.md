title: Makefile
teaser:
  Mobile 100 (Flag system) task writeup from RCTF 2015. Android app decompiling, changing smali
  code and many other interesting things :)
---

[[toc]]

## Example

``` make
CC = gcc
LD = $(CC)
CFLAGS = -I./include -g
LDFLAGS = -levent
SOURCE_FILES = $(wildcard *.c)
OBJECT_FILES = $(SOURCE_FILES:%.c=%.o)

all: $(TARGET)

$(TARGET): $(OBJECT_FILES)
	$(LD) $^ -o $@ $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	@rm -f $(OBJECT_FILES) $(TARGET)
```

## All *.c or *.o files

``` make
# all *.c files in directory
SOURCE_FILES = $(wildcard *.c)

# replace .c to .o
$(patsubst %.c,%.o,$(wildcard *.c))

# also replace .c with .o
$(VARIABLE:%.o=%.c)

# matching any number of any characters
%
```

## Variable assigment

``` make
# value expanded when the variable is used
VARIABLE = value

# value expanded at declaration time
VARIABLE := value

# set variable only if it doesn't have a value
VARIABLE ?= value

# append supplied value to the existing value
VARIABLE += value
```

## Automatic variables

``` make
$@   # the current target
$<   # first dependency
$^   # all dependencies
```

| test  | test  |
|-------|-------|
| Hello | World |