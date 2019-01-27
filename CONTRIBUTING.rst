.. _newcomers:

*********************************************
Newcomer's Guide (How to Contribute to SunPy)
*********************************************

Welcome to the SunPy newcomers guide.
If you have come across this page, you just might be new to SunPy.
We aim to be a comprehensive Python package that allows solar physicists to deep dive in the vast amount of solar data available.

Firstly, we want to thank you for your interest in contributing to SunPy!
SunPy is an open project that encourages everyone to contribute in any way possible.

The people who help develop or contribute to SunPy are varied in ability and experience with the vast majority being volunteers who dedicate time each week.
We pride ourselves on being a welcoming community and we would love to have you become a part of our community.

Although this document mainly focuses on how to make contributions to SunPy's code and documentation, there are other ways to get involved with the SunPy community.

If you have any questions, comments or just want to say hello, we have online chat on `Matrix`_ which requires no registration or a `Google Group`_ which you message.

.. _Matrix: https://riot.im/app/#/room/#sunpy-general:matrix.org
.. _Google Group: https://groups.google.com/forum/#!forum/sunpy

How to Contribute to SunPy
==========================

Since SunPy is the work of many volunteers, we are always looking for more people to contribute however they can and to join our community.

Non-Code
--------

A common misconception (which applies to any package) is that all we really want is some Python code, in fact, we do not require only code contributions!
If you do not have the time or the desire to code, we have severals of areas where we can use help.

Reporting Issues
^^^^^^^^^^^^^^^^

If you use SunPy and stumble upon a problem, the best way to report it is by opening an `issue`_ on our GitHub issue tracker.
This way we can help you work around the problem and hopefully fix the problem!

You will need to sign into `GitHub`_ to report an issue and if you are not already a member of Github, you will have to join.
Joining GitHub will make it easier to report and track issues in the future.

If you do not want to join Github, then another way to report your issue
is email the SunPy developers list `sunpy-dev@googlegroups.com`_.

When reporting an issue, please try to provide a short description of the issue with a small code sample, this way we can attempt to reproduce the error.
Also provide any error output generated when you enchoutered the issue, we can use this information to debug the issue.
For a good example of how to do this see issue `#2879`_.

If you are making a feature request, please post as much information as possible regarding the feature you would like to see in SunPy.

We provide GitHub templates for both of these types of issue.
Each one has several sections that detail the type of information we are seeking.

.. _issue: https://github.com/sunpy/sunpy/issues
.. _sunpy-dev@googlegroups.com: https://groups.google.com/forum/#!forum/sunpy-dev
.. _#2879: https://github.com/sunpy/sunpy/issues/2879

Documentation
^^^^^^^^^^^^^

SunPy has `online documentation`_ and we try to make sure its as comprehensive as possible.
This documentation contains the API of SunPy but also a user guide, an example gallery and developer documents.

However, documentation for any project is a living document.
It is never complete and there are always areas that could be expanded upon or could do with proof reading to check if the text is easy to follow and understandable.
If parts are confusing or difficult to follow, we would love suggestions or improvements!

.. _online documentation: http://docs.sunpy.org/en/latest/index.html

Reviewing a Pull Request
^^^^^^^^^^^^^^^^^^^^^^^^

We at any one time have a variety of `pull requests_` open and getting reviews is important.
Generally the more people that can look over a pull request the better and we encourage everyone to do so.

.. _pull requests: https://github.com/sunpy/sunpy/pulls

Code
----

If you would prefer to code instead, we have several repositories you can investigate.
The main one is the SunPy repository with where all the known `issues`_ with SunPy are detailed.
Each issue should have a series of labels that provide some information about the effort required to tackle that issue.

If you are unsure where to start we suggest the `Package Novice label`_.
These are issues that have been deemed a good way to be eased into SunPy and are achievable with little understanding of the SunPy codebase.
Please be aware that this does not mean the issue is "easy", just that you do not need to be aware of the underlying structure of SunPy.

We also tag issues for specific events such as  `Hacktoberfest`_ under the `Hacktoberfest label`_.
The scope of the issues should be appropriate for that specific event.
We do particpate in several other events but right now we do not have decidated labels.
So please use the above labels for starting issues!

In addition, we have several other repositories that have open issues and you might find these more interesting than the main repository.

Python:

* `ndcube <https://github.com/sunpy/ndcube>`_
* `drms <https://github.com/sunpy/drms>`_
* `radiospectra <https://github.com/sunpy/radiospectra>`_
* `ablog <https://github.com/sunpy/ablog>`_
* `irispy <https://github.com/sunpy/irispy>`_
* `sunkit-image <https://github.com/sunpy/sunkit-image>`_

CSS/HTML/Python:

* `sunpy-sphinx-theme <https://github.com/sunpy/sunpy-sphinx-theme>`_
* `sunpy.org <https://github.com/sunpy/sunpy.org>`_

.. _issues: https://github.com/sunpy/sunpy/issues
.. _Package Novice label: https://github.com/sunpy/sunpy/issues?q=is%3Aissue+is%3Aopen+label%3Apackage-novice
.. _Hacktoberfest: https://hacktoberfest.digitalocean.com/
.. _Hacktoberfest label: https://github.com/sunpy/sunpy/issues?q=is%3Aissue+is%3Aopen+label%3AHacktoberfest

Development environment
=======================

The instructions in this following section are based upon three resources:

* `Astropy Dev Workflow http://docs.astropy.org/en/latest/development/workflow/development_workflow.html>`_
* `Astropy Dev environment <http://docs.astropy.org/en/latest/development/workflow/get_devel_version.html#get-devel>`_
* `Astropy Pull Request Example <http://docs.astropy.org/en/latest/development/workflow/git_edit_workflow_examples.html#astropy-fix-example>`_

These contain more in-depth details that apply here but replacing ``astropy`` with ``sunpy``.
**We strongly recommend a read of these links.**

Setting up a work environment
-----------------------------

In order to start coding you will need a local Python environment and we would recommend using `Anaconda_` or `miniconda`_ (shortened to conda from here on).
This method will bypass your operating system Python packages and makes the entire process easier.

The first step is to install the version of conda that corresponds to your operating system (`instructions here`_).
Next we will want to setup the conda environment and we will need to add the `conda-forge_` channel as a prerequisite:

.. code:: bash

    conda config --add channels conda-forge
    conda create -n sunpy-dev sunpy
    source activate sunpy-dev

This will create a new conda environment called `sunpy-dev` and install the latest version of SunPy from the conda-forge channel.
The next step is remove the conda version of SunPy and install the development version of SunPy.
This will require that `git`_ be installed.

If you have a `GitHub`_ account, we suggest that you `fork`_ the `SunPy repository`_ (the fork button is to the top right) and **use that url for the clone step** below.
This will make submitting changes easier in the long term for you:

.. code:: bash

    conda remove sunpy
    git clone https://github.com/sunpy/sunpy.git sunpy-git
    cd sunpy-git
    pip install -e .[all]

Now you have the latest version of SunPy installed and are ready to work on it using your favorite editor!
Ideally, when you start making changes you want to create a git branch:

.. code:: bash

    git checkout -b my_fix

You can change ``my_fix`` to anything you prefer.
If you get stuck or want help, just `ask here`_!

.. _Anaconda: https://www.anaconda.com/
.. _miniconda: https://conda.io/miniconda.html
.. _instructions here: https://conda.io/docs/user-guide/install/index.html
.. _conda-forge: https://conda-forge.org/
.. _git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
.. _GitHub: https://github.com/
.. _fork: https://guides.github.com/activities/forking/
.. _SunPy repository: https://github.com/sunpy/sunpy
.. _ask here: https://riot.im/app/#/room/#sunpy-general:matrix.org

Astropy helpers
---------------

Within SunPy is a folder called `astropy_helpers_` and this is a git submodule.
It is very common issue that this not setup correctly and gets added to your commits.

So we recommend that you always run this at the start:

.. code:: bash

    git submodule update --init

This will resolve any differences in the `astropy_helper` folder on your machine.

.. astropy_helpers: https://github.com/astropy/astropy-helpers

Send it back to us
------------------

Once you have some changes you would like to submit, you will need to commit the changes.
This is a three stage process:

1. Use `git status` to see that the only changes locally are the right ones.
2. Use `git add <path to file>` to add the changes to `git`.
3. Use `git commit -m <message>` to label those changes.

Where you replace `<message>` with some text of the work you have done.
We strongly recommend having a good commit message and this `commit guide`_ is worth reading.

Next step is to open a pull request on GitHub.
If you are new to pull requests here is a `friendly guide`_.
Go to the `pull requests_` tab on **your fork** and pressing the large green `New pull request` button.
Now on the right side from the box marked `compare` you can select your branch.
Do one final check to make sure the code changes look correct and then press the green `Create pull request` button.

When you open your pull request, we have a GitHub template that will guide you on what to write in the message box.
Please fill this in and title the pull request.
Now the final step is to press the green `Create pull request` button.

As soon as you do this, you will be greeted by a message from `sunpy bot` as well as several continuous integration checks.
These are explained in depth on our :ref: `Version Control <version_control>` page.
But what is important to know is that these run a series of tests to make sure that the changes do not cause any new errors.
Now we (the SunPy community) can review the code and offer suggestions and once we are happy, we can merge in the pull request.

If you do not have time to finish what you started on or ran out of time during a sprint and do not want to submit a pull request, you can create a git patch instead:

.. code:: bash

    git format-patch master --stdout > my_fix.patch

You can rename ``my_fix`` to something more relevant.
This way, you still get acknowledged for the work you have achieved.
Now you can email this patch to either the  `Google Group`_ or `a SunPy contributor`_.

Just remember, if you have any problems get in touch!

.. _commit guide: https://chris.beams.io/posts/git-commit/
.. _friendly guide: https://guides.github.com/activities/hello-world/
.. _Google Group: https://groups.google.com/forum/#!forum/sunpy
.. _a SunPy contributor: stuart@mumford.me.uk
