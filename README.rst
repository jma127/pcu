================================
PCU: Programming Contest Utility
================================

Comprehensive suite for competitive programming

https://github.com/jma127/pcu

PCU is licensed under the BSD 3-clause license (see LICENSE file).


Installation
============

All installations require Python 3.6+ with setuptools.

Pip
---

The simplest method::

    pip3 install pcu

Source
------

Almost as simple::

    git clone https://github.com/jma127/pcu.git
    cd pcu
    python3 setup.py install


Venv Install
------------

If you'd like to keep dependencies separate from your system python, then you
may use the venv_install.py script::

    git clone https://github.com/jma127/pcu.git
    cd pcu
    python3 venv_install.py


Usage
=====

After installing PCU with the tool above, you may run the tools from whichever
directory you wish to work in. The basic format for the pcu tool is::

    $ pcu command problem

The ``command`` field is the utility you would like to use. See the `Available
Tools`_ section for more information. The ``problem`` field should be the name
of the problem you're currently working on.

Here is an example to get you started. Here (and in the rest of this README), we
are trying to solve the particularly challenging ``add_two_numbers`` problem,
where the program should read two numbers from stdin and write their sum to
stdout::

    # initialize the problem
    # (by default, using the ``cpp`` environment)
    # this also creates the source file add_two_numbers.cpp using a template
    pcu make add_two_numbers

    # add the sample input and output
    pcu setin add_two_numbers sample < sample_input.txt
    pcu setans add_two_numbers sample < sample_expected_output.txt

    # then, edit your source file however you like
    vim add_two_numbers.cpp

    # run your program (against the sample input, since you added it above)
    pcu run add_two_numbers


Available Tools
===============

Initialization and Source File Generation
-----------------------------------------

The command for initializing a problem is ``pcu make <problem>``. By default,
this will generate a code skeleton according to predefined templates_ in your
current working directory. The name of the source file is specified by the
current environment_'s ``source_file`` setting.

To make the source file for the ``add_two_numbers`` problem in the default
environment::

    pcu make add_two_numbers

To make the source file for the ``add_two_numbers`` problem in the Java
environment::

    pcu make -e java add_two_numbers

If you already have the source file, you can use the ``-S`` flag (short for
``--nosrc``) to skip creating the source file (otherwise, PCU will overwrite
your precious code).

If you've already initialized the problem and just want to generate a new source
file, you can use the ``-C`` flag (short for ``--noclean``) to preserve the
environment and just generate the source file.

Test Case Management
--------------------

You can use PCU to manage your custom test cases for a problem. This is
particularly useful when combined with ``pcu run`` (see below). In PCU, each
test case has a unique identifier (set by the user) and may have an input file
and an expected output (answer) file.

Adding and Editing Test Cases
`````````````````````````````

The two commands for adding and editing test data are:

* ``pcu setin <problem> <testcase>``
* ``pcu setans <problem> <testcase>``.

Let's say we are still working on the problem ``add_two_numbers``, and we are
trying to add the sample input and output (which we want to call
``sample_test``). To add the sample input, run::

    pcu setin add_two_numbers sample_test
    # Now you will be prompted to enter the input.

To add the sample output, run::

    pcu setans add_two_numbers sample_test
    # Now you will be prompted to enter the expected output.

Of course, both these commands work with stdin redirection::

    pcu setin add_two_numbers sample_test < sample_input.txt
    pcu setans add_two_numbers sample_test < sample_expected_output.txt

Viewing Test Cases
``````````````````

The commands for viewing test cases are:

* Viewing list of test cases: ``pcu info <problem>``
* Get a specific test case's input: ``pcu getin <problem> <testcase>``
* Get a specific test case's expected output: ``pcu getin <problem> <testcase>``

Example with our ``add_two_numbers`` problem::

    # Will show us what test cases exist for "add_two_numbers"
    pcu info add_two_numbers

    pcu getin add_two_numbers sample_test > sample_in.txt
    pcu getans add_two_numbers sample_test > sample_ans.txt

Deleting Test Cases
```````````````````

The command for deleting test cases is ``pcu delcases <problem> <testcase>``.
Example::

    pcu delcases add_two_numbers sample_test

You may specify more than one test case::

    pcu delcases add_two_numbers sample_test another_test

Or omit the ``testcase`` argument entirely to delete *all* testcases::

    pcu delcases add_two_numbers

Compiling and Running
---------------------

After you have created the source file, added some test cases, and written up
your solution, you'd naturally like to run your code. The command for this is
``pcu run <problem>``. Example::

    pcu run add_two_numbers

The command compiles your program and, if compiled successfully, runs it against
all test cases. To only test against specific test cases, you can specify the
test case names after the problem name::

    pcu run add_two_numbers sample_test another_test

If all you want to do is compile, use the ``pcu comp <problem>`` command.
Example::

    pcu comp add_two_numbers

You may modify how PCU compiles and runs your program via environment_ settings.


Viewing Output
``````````````

``pcu run`` prints out per-test-case results, including the status (e.g.
correct, wrong answer, runtime error), diffs between expected and actual output,
and stderr output from your program. However, it does *not* print the full
output of the program for each test case. The commands for getting the output
for a specific test case is ``pcu getout <problem> <testcase>`` (similarly, to
get stderr, run ``pcu geterr <problem> <testcase>``). Example::

    pcu getout add_two_numbers sample_test > my_sample_out.txt
    pcu geterr add_two_numbers sample_test > my_sample_stderr.txt

Test Case Generation
--------------------

If you would like to programmatically generate test data for problems, you may
use the ``testgen`` command. This module uses a user-specified executable (such
as a script or a binary) to create testcases. The command for test case
generation is ``pcu testgen <problem> <generator_executable>``.  The optional
argument ``-n`` specifies the number of tests that should be generated, and the
optional argument ``-p`` specifies the prefix for the generated test case names.

To generate 50 test cases for ``add_two_numbers`` with the executable
``gen_test.py``::

    $ pcu testgen -n 50 add_two_numbers gen_test.py


Make sure that your generator is actually executable (e.g. with ``chmod 755`` in
Unix).

Generator Executable Specification
``````````````````````````````````
Generator executables are passed two command-line arguments:

* ``seq_num``: the number of the current test case to be generated. This
  argument is not very useful unless you're trying to generate test cases with
  different characteristics (e.g. 10 "small" cases and 10 "large" cases).
* ``seed``: a seed (different for each test case) that can be used for randomly
  generating test data. Guaranteed to be nonnegative and to fit within a 32-bit
  signed integer.

The generator executable should then output the test case input data to stdout,
and the expected output (answer) to stderr. Below is an example of a test
generator for ``add_two_numbers``::

    #!/usr/bin/env python3
    import random, sys
    random.seed(sys.argv[2]) # the second argument is the random seed
    a, b = random.randint(0, 1000000), random.randint(0, 1000000)
    print(a, b)
    print(a + b, file=sys.stderr)

Help
----

You may run ``pcu -h`` to get a list of commands with descriptions, and ``pcu
<command> -h`` to get help for any individual command.


Settings
========

PCU is configurable via the following (case-sensitive) settings:

* ``user``: your name. You may use ``os_username`` to tell PCU to use your
  system username.
* ``default_env``: the default environment_.
* ``datetime_format``: a `strftime <http://strftime.net/>`_-compatible format
  string to use in PCU-generated timestamps.
* ``max_lines_output``: maximum number of output/diff lines to show for each
  testcase in ``pcu run``.
* ``max_lines_error``: maximum number of stderr lines to show for each testcase
  in ``pcu run``.
* ``envs``: the environments available to PCU. Specified as a YAML mapping of
  environment name to environment settings.

Default values for these settings are in `pcu/static/default_settings.yaml
<https://github.com/jma127/pcu/blob/master/pcu/static/default_settings.yaml>`_.
You may override defaults by specifying your own settings in
``~/.pcu/settings.yaml``. YAML references can be googled (`here
<http://yaml.org/>`_ is a basic one).

Environment
-----------

An environment is simply a coherent group of settings for a specific language,
contest, etc. While the settings above are *global* settings, the following are
*per-environment* settings:

* ``template_file``: name of the environment's template file. This is required
  to use ``pcu make``. See the Templates_ section for more information.
* ``compile_timelimit_msec``: number of milliseconds the compiler gets.
* ``run_timelimit_msec``: number of milliseconds for each test case before a
  judgement of "Time Limit Exceeded".
* ``format_strictness``: either ``strict`` or ``lax``.
    - ``strict`` tells ``pcu run`` to check for an exact match between expected
      and actual output.
    - ``lax`` tells ``pcu run`` to ignore whitespace errors when checking
      output.
* ``aliases``: a list of alternative names for this environment.

For the following per-environment settings, you may use ``${PCU_PROBLEM_NAME}``
to refer to the current problem's name:

* ``source_file``: name of the source file (e.g. output of ``pcu make``).

For the following per-environment settings, in addition to
``${PCU_PROBLEM_NAME}``, you may use ``${PCU_SOURCE_FILE}`` to refer to the
source file name, and ``${PCU_SOURCE_FILE_NOEXT}`` to refer to the source file
name without the extension:

* ``compile_command``: command to compile the program. Note that this is passed
  as raw shell input, and you are solely responsible for any security
  implications.
* ``run_command``: command to run the program. Same caveat as above.
* ``input_file``: file where the program will expect its input data.
  ``PCU_STDIN`` is a special value meaning that the program reads from stdin.
* ``output_file``: file where PCU will expect the program to output its results.
  ``PCU_STDOUT`` is a special value meaning that the program writes to stdout.


Templates
=========

``pcu make`` uses templates to generate source files. A template looks very much
like a source file, except that ``pcu make`` will substitute all parameter names
with their respective values. The following are valid template parameters:

* ``${PCU_USER}``: the ``user`` setting.
* ``${PCU_DATETIME}``: the current date and time (formatted via the
  ``datetime_format`` setting)
* ``${PCU_PROBLEM_NAME}``: the current problem's name.
* ``${PCU_ENV_NAME}``: the current environment's name.
* ``${PCU_COMPILE_TIMELIMIT_MSEC}``: the ``compile_timelimit_msec`` environment
  setting.
* ``${PCU_RUN_TIMELIMIT_MSEC}``: the ``run_timelimit_msec`` environment setting.
* ``${PCU_FORMAT_STRICTNESS}``: the ``format_strictness`` environment setting.
* ``${PCU_SOURCE_FILE}``: the current problem's source file name.
* ``${PCU_SOURCE_FILE_NOEXT}``: the above, without the extension.
* ``${PCU_COMPILE_COMMAND}``: the shell command used to compile the program.
* ``${PCU_RUN_TIMELIMIT_MSEC}``: the shell command used to run the program.
* ``${PCU_INPUT_FILE}``: the current problem's input file name.
* ``${PCU_OUTPUT_FILE}``: the current problem's output file name.

Templates are per-environment, and PCU uses the environment's ``template_file``
setting to search for the template in ``~/.pcu/templates/``. If not found, PCU
will look for it in `pcu/static/default_templates/
<https://github.com/jma127/pcu/tree/master/pcu/static/default_templates>`_.
