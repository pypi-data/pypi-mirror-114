# dd-firmware

## What is dd-firmware?

dd-firmware is a simple script for terminal use.  It queries dd-wrt.com for router firmware based on user input and writes it to the present working directory. 

## System Requirements

* python3


## Installation

```pip install dd-firmware```

## Usage

To use dd-firmware:

### Basic / Current Day

```dd-firmware [router]```

Example: dd-firmware r7000; uses fuzzy regex match


### Arguments

```-f or --five```

prints the last five firmware release dates and allows you to pick from within
