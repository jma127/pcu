================================
PCU: Programming Contest Utility
================================

Comprehensive suite for competitive programming

https://github.com/jma127/pcu

PCU is licensed under the Mozilla Public License, version 2.0 (see LICENSE
file)

Download
========

The PCU git repository can be obtained by::

    $ git clone git://github.com/jma127/pcu.git

A ZIP version of the project folder is also available at

https://github.com/jma127/pcu/archive/master.zip

Installation
============

PCU installs itself by placing a launch script in your ``PATH`` and copying the
defaulttemplates folder into the templates folder. A tool is provided in the
project directory for this purpose::

    $ python install.py

You should not move or delete the project directory after installation, as the
source files and templates are not copied to your ``PATH``.

Usage
=====

After installing PCU with the tool above, you may run the tools from whichever
directory you wish to work in. The basic format for the pcu tool is::

    $ pcu command [optargs] problem

The ``command`` field is the utility you would like to use. See the `Available
Tools`_ section for more information. The ``problem`` field should be the name
of the problem you're currently working on. For example, the command to compile
the source file for the problem ``problem1`` is::

    $ pcu comp problem1

The default language, I/O mode, and file parameters are determined in the
``settings.py`` file (see Settings_ for more info). To declare/change the
language or I/O mode for a problem, you may include `optional arguments`_. For
example, the command to compile the Python source file (``problem1.py``) for
the problem ``problem1`` is::

    $ pcu comp -l py problem1

Available Tools
===============

Note: most of these commands may be combined with the optional arguments `-l`
and `-m` described in the `Optional Arguments`_ section.

Source File Generation
----------------------

PCU can generate a code skeleton according to predefined templates (see the
Templates_ section). The command argument for source file generation is
``make``. This will generate a source file containing a code skeleton named
``problem.langext`` in the current directory.

To make the source file for ``problem1`` in the default language and I/O mode::

    $ pcu make problem1

To make the source file for ``problem2`` in Java and I/O mode ``stdio``::

    $ pcu make -m stdio -l java problem2

Program Compilation
-------------------

PCU can compile a source file and print the result (errors and warnings) for
you with the ``comp`` command argument. This will search for a file in the
current directory named ``problem.langext`` and attempt a compilation with the
command and time constraints in the settings_ file.

To compile the source file for ``problem1`` in the default language::

    $ pcu comp problem1

To compile the C source file for ``problem2``::

    $ pcu comp -l c problem2

Test Case Management
--------------------

You can use PCU to manage your custom test cases for a problem. This is
particularly useful when combined with the testing module below. In PCU, each
test case has a unique identifier (set by the user) and may have an input file
and an expected output (answer) file. The test case command arguments are:

* ``setin``: set the input for a test case
* ``setans``: set the expected output for a test case
* ``getin``: get the input for a test case
* ``getans``: get the expected output for a test case

However, these commands must be invoked with a special ``testid`` argument,
where ``testid`` is the identifier of the test case you wish to access or
manipulate.

The ``set[in/ans]`` command will read console input (stdin) from the user until
EOF is inputted (Ctrl-D in Max/Linux, Ctrl-Z in Windows). The ``get[in/ans]``
command will print the input/answer file (if it exists) to the console output
(stdout).

The ``-f filename`` argument may be used to copy the output to a file instead
of printing the file to the screen, in the case of a `get` command, or to read
the input from a file instead of the console, in the case of a ``set[in/ans]``
command.

Test case data may be overwritten by calling ``setin`` or ``setans`` with the
same ``testid``. If the ``get[in/ans]`` command is combined with the ``-f``
option, any data in the provided file will be overwritten.

To set the input for test case ``tc1`` of ``problem1``::

    $ pcu setin problem1 tc1

To set the expected output for test case ``tc1`` of ``problem1`` with a
provided answer file ``ans1``::

    $ pcu setans -f ans1 problem1 tc1

To retrieve the input for test case ``tc1`` of ``problem1``::

    $ pcu getin problem1 tc1

To retrieve the expected output for test case ``tc1`` of ``problem1`` and copy
it to ``problem1.ans``::

    $ pcu getans -f problem1.ans problem1 tc1

Test Case Generation
--------------------

If you would like to programmatically generate test data for problems, you may
use PCU's ``testgen`` module. This module uses a user-specified executable
(such as a script or a binary) to create testcases. The command argument for
test case generation is ``testgen``. It also takes a required argument, the
generator executable, and an optional argument ``-n``, which specifies the
number of tests that should be generated.

To generate 50 test cases for ``problem1`` with the executable
``gentests.py``::

    $ pcu testgen -n 50 problem1 gentests.py

Generator Executable Specification
``````````````````````````````````
Each executable is passed two command-line arguments:

* ``number``: the number of the current test case to be generated
* ``seed``: an arbitrary seed (different for each test cases) that can be used
  for randomly generating test cases, between 0 and 2147483647

The executable should then output the test case input data to stdout, and the
expected output (answer) to stderr. Below is an example of a test generator for
a "sum two integers" problem::

    #!/usr/bin/python
    import random, sys
    random.seed(sys.argv[2]) # the second argument is the random seed
    a, b = random.randint(0, 1000000), random.randint(0, 1000000)
    print a, b
    print >> sys.stderr, a + b

Program Execution/Testing
-------------------------

PCU has a program execution module that can compile and run your program
against custom test cases (set by the `test case management`_ module) with time
constraint and run command defined in the settings_ file. This module is usable
with the command argument ``run``. After execution, it can print the program
output and stderr (in addition to stdout if the problem is in file mode). It
can detect runtime errors and time limit errors for each test case. In
addition, if answer files are specified for test cases, it will check the
program output against the expected output and detect wrong answers, whitespace
errors, and correct answers.

After execution, you may wish to review the program output. PCU provides the
following command arguments to print the output to the screen:

* ``getout``: for program output
* ``getstdout``: for stdout (only in file I/O mode)
* ``getstderr``: for stderr

Like the test case management commands, these commands must be combined with
the ``-t testid`` optional argument which specifies the test case from which
you would like to retrieve output. Also, the ``-f filename`` argument may be
used to copy the output to a file instead.

To run the program for ``problem1`` against all test cases with the default
language and I/O mode::

    $ pcu run problem1

To run the C++ file I/O program for ``problem1`` against all test cases::

    $ pcu run -l cpp -m file problem1

The ``get[out/stdout/stderr]`` command arguments are similar to the `test case
management`_ commands: see that section for examples.

Optional Arguments
------------------

In addition to the file and test case arguments, you may use ``-l langext`` to
set or change the current language extension. The default languages available
are C (``c``), C++ (``cpp``, ``cc``), Java (``java``), Python (``py``), and
Shell (``sh``). You may add more languages and language extensions in the
settings_ file.

The other option argument is ``-m mode``, which allows you to change the I/O
mode. There are two modes: ``file`` and ``stdio``. ``stdio`` is for problems
that require input and output from stdin and stdout, while ``file`` is for
problems that read and write to files.

PCU stores the `-m` option in a special hidden file for each problem, so you do
not have to repeat the optional argument for each tool you wish to use.

These options must be used in conjunction with a command argument, such as
``make`` or ``run``.

Help
----

You may run the following command to get a short description of available
options::

    $ pcu -h

Settings
========

PCU uses a python source file named ``settings.py`` to manage user preferences.
This file includes all program options, as well as their default values.
``settings.py`` is commented with brief descriptions of all settings. To modify
a setting, simply change the default to your preferred value. Note that all
text settings are case-sensitive.

Templates
=========

The ``templates`` folder contains source file templates for various languages
and I/O modes. You may modify the templates to suit your individual uses. In
addition, you may add templates by moving the template source file to the
folder and renaming it ``mode.langext`` (see the included templates).

PCU's source file generator comes with limited support for variable symbols,
prefixed by ``$``. The symbols currently available are:

* ``$INFILE``: program input file name (if problem mode is file I/O)
* ``$OUTFILE``: program output file name (if problem mode is file I/O)
* ``$SRCFILE``: program source file name (equal to ``$PROB.$EXT``)
* ``$PROB``: problem name
* ``$EXT``: language extension (``.cpp``, ``.java``, etc.)
* ``$USER``: PCU user name (changeable in ``settings.py``)
