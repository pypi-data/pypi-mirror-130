# Safe Action Model Learning

SAM learner is an algorithm to efficiently and *safely* learn action models of STRIPS problems.

This repository contains two variations of the algorithm:
* The classic SAM learning algorithm.
* Lightweight version of ESAM learning algorithm.

The code is also available as a package to download in [PyPI](https://pypi.org/project/sam-learner/).

## Requirements:

The repository's code is currently running using [Python](https://python.org) >= 3.8.
In addition, This code is currently depending on the on version 1.3 of [pyperplan](https://github.com/aibasel/pyperplan).

## Installation:

From the Python package index (PyPI):

    pip install sam-learner
   
## Features:

The repository offers two variants of the SAM learning algorithm, the classical SAM learning algorithm as well as a 
lightweight version of the *Extended* SAM learning algorithm.

### Classical SAM Learning:

* Learn *lifted* action model of classical PDDL problems.
* Currently, supports PDDL-1.2 only.
* Export learned domain via domain export functionality.

### Extended SAM Learning:

* Learn *lifted* action model of classical PDDL problems.
* Extends SAM to also learn action models in case that there is an ambiguity in the actions' execution process.
* Currently, supports PDDL-1.2 only.
* Export learned domain via domain export functionality.

### New Feature:

Now the code outputs trajectories in a format that FAMA action model learning can read and translate.