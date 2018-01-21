# CSE 4/589: PA2 AutoGrader

Note that you need to follow the instructions below **ONLY** if you want to run the grader from source for debugging purposes or you are trying to re-package after making changes or package it into a binary for a non-Linux platform.

Typically, you do **NOT** need to specifically provide even the binary version (or a link to download it) to the students. The main assignment description/handout provided to students already contains the download link and instructions for its usage.

## Setup
You need to follow the steps below only if you want to run the grader from the source.

```bash
$ git clone --no-checkout https://github.com/cse4589/cse4589-pa2.git
$ cd cse4589-pa2
$ git config core.sparseCheckout true
$ echo 'Grader' >> .git/info/sparse-checkout
$ git checkout master
```

## Run
```bash
$ cd Grader
```

The individual tests make use of the _run_experiments_ script to actually run the student submissions under the simulator. However, it can be invoked directly as:
```bash
$ python run_experiments.py -h
```

The individual tests can be run as:
```bash
$ python sanity_tests.py -h
$ python basic_tests.py -h
$ python advanced_tests.py -h
```

The binary versions (created using the steps detailed below) can be run similarly as:

```bash
$ ./run_experiments -h
$ ./sanity_tests -h
$ ./basic_tests -h
$ ./advanced_tests -h
```

## Convert to Binary
We make use of the [pyinstaller](http://www.pyinstaller.org/) package to convert AutoGrader's client side python scripts into a single executable binary.

You need to first obtain the source of the grader, using instructions listed above under the [Setup](https://github.com/cse4589/cse4589-pa3/tree/master/Grader/local#setup) section. To convert to binary, execute the following with the ```Grader``` as the root directory.

```bash
$ pyinstaller --onefile run_experiments.py
$ pyinstaller --onefile sanity_tests.py
$ pyinstaller --onefile basic_tests.py
$ pyinstaller --onefile advanced_tests.py
```

If everything goes well, the executables will be will be created in the ```Grader/dist``` directory. You can upload the binaries somewhere they can be publicly downloaded from.

***
<img src="https://cse4589.github.io/assets/site/images/UB_BLU_RGB.png" width=30></img>
In all likelihood, there is no need for this conversion as pre-compiled binaries are already available for UB students to be downloaded. The download and setup is taken care by the template scripts which are documented in the assignment handout/description.
***
