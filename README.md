# llocker - Applying logic Locking to Various Circuits

## Purpose

This project was intended to familiar myself with RTL, Locking Locking Schemes, and the [OSS Cad Suite](https://github.com/YosysHQ/oss-cad-suite-build)

This project's mains goals where to:

1. Identify some test circuit designs
1. Push those designs as far along the IC lifecycle as possible
1. Apply a variety of logic locking schemes to said designs
1. Explore the artifacts generated by the process to better understand how to quantify intellectual property protection in IC design

## Overview

The repository contains the results of applying a series of logic locking algorithms to 6 small Verilog circuits:

- kmStLN
- koStln
- kSLn
- wmStLN
- woStLN
- c432

For each example circuit, we attempted to apply the following algorithms:

- full_lock
- full_lock_mux
- lut_lock
- mux_lock
- random_lut_lock
- sfll_flex
- sfll_hd
- trll
- tt_lock
- tt_lock_sen
- xor_lock

---

## 1. Starting from Scratch

---

### Prerequisites

This project was built inside a Windows 10 WSL Ubuntu 20.04.6 env. I expect it should be simple to replicate in any *NIX environment that can satisfy the following requirements:

1. [OSS Cad Suite](#oss-cad-suite)
1. [Python 3](#python-3)
1. Graphviz (for the `dot` command line tool)
1. Make

#### OSS Cad Suite

Per the [OSS CAD Suite](https://github.com/YosysHQ/oss-cad-suite-build) github page:

> The OSS CAD Suite  is a binary software distribution for a number of open source software used in digital logic design.

Most important to this exercise, it includes a version of [Yosys](https://github.com/YosysHQ/yosys) (a RTL synthesis suite). Installation is relatively straight forward and is detailed on the OSS CAD Suite github page. In a nutshell: grab the most recent archive, extract it somewhere, and make sure its `bin` directory is in your path.

#### Python 3

The Python requirements can be found below:
![[requirements.txt]]

Circuitgraph, lark, networkx, and python-sat support to the RTL manipulation used by the logic locking code. These can be installed from pypi using pip.

The central Python Library: [logiclocking](https://circuitgraph.github.io/logiclocking/locks.html) is included as a submodule to this repository. See its documentation for details and citations for each logic locking algorithms used.

I use Jinja2 and MarkupSafe to generate the reports at the end of the scripting process.

**Note before installing these preqs:**
You have two options for installing the PiPy modules: system-wide or in a python virtual environment. My instructions below detail the later.

#### Graphviz

Installing this program is going to differ depending on your environment. I installed it using apt:

`apt-get install graphviz`

#### Make

Whatever stock version of gnu make is available on your system should be sufficient.

---

## 2. Running the Scripts

---

**New install**
The following two steps only need to be done once, when starting from scratch:

Step 1. Clone this repo:

`git clone https://github.com/The-Chairman/LogicLockingDemo.git --recurse-submodules`

Step 2. Initialize a python virtual environment:

`cd LogicLockingDemo`
`python -mvenv venv`
`source venv/bin/activate`

Step 3. Install python dependencies:

---

## 3. Viewing Results

---

# Attribution

HTML templates used for NIST Science Day 2024 Licensed under The Creative Commons 3.0 License [HTML5 UP](https://html5up.net/)


