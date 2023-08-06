<!--
  THIS FILE IS EXCLUSIVELY MAINTAINED IN THE NAMESPACE ROOT PACKAGE. CHANGES HAVE TO BE DONE THERE.
-->
# updater portion of ae namespace package

[![GitLabPipeline](https://img.shields.io/gitlab/pipeline/ae-group/ae_updater/master?logo=python)](
    https://gitlab.com/ae-group/ae_updater)
[![PyPIVersion](https://img.shields.io/pypi/v/ae_updater)](
    https://pypi.org/project/ae-updater/#history)

>The portions (modules and sub-packages) of the Application Environment for Python are within
the `ae` namespace and are providing helper methods and classes to develop
full-featured applications with Python.

[![Coverage](https://ae-group.gitlab.io/ae_updater/coverage.svg)](
    https://ae-group.gitlab.io/ae_updater/coverage/ae_updater_py.html)
[![MyPyPrecision](https://ae-group.gitlab.io/ae_updater/mypy.svg)](
    https://ae-group.gitlab.io/ae_updater/lineprecision.txt)
[![PyLintScore](https://ae-group.gitlab.io/ae_updater/pylint.svg)](
    https://ae-group.gitlab.io/ae_updater/pylint.log)

[![PyPIImplementation](https://img.shields.io/pypi/implementation/ae_updater)](
    https://pypi.org/project/ae-updater/)
[![PyPIPyVersions](https://img.shields.io/pypi/pyversions/ae_updater)](
    https://pypi.org/project/ae-updater/)
[![PyPIWheel](https://img.shields.io/pypi/wheel/ae_updater)](
    https://pypi.org/project/ae-updater/)
[![PyPIFormat](https://img.shields.io/pypi/format/ae_updater)](
    https://pypi.org/project/ae-updater/)
[![PyPIStatus](https://img.shields.io/pypi/status/ae_updater)](
    https://libraries.io/pypi/ae-updater)
[![PyPIDownloads](https://img.shields.io/pypi/dm/ae_updater)](
    https://pypi.org/project/ae-updater/#files)


## installation


execute the following command to use the ae.updater module in your
application. it will install ae.updater into your python (virtual) environment:
 
```shell script
pip install ae-updater
```

if you instead want to contribute to this portion then first fork
[the ae_updater repository at GitLab](https://gitlab.com/ae-group/ae_updater "ae.updater code repository"),
then pull it to your machine and finally execute the following command in the root folder
of this repository (ae_updater):

```shell script
pip install -e .[dev]
```

the last command will install this module portion into your virtual environment, along with
the tools you need to develop and run tests or to extend the portion documentation.
to contribute only to the unit tests or to the documentation of this portion replace
the setup extras key `dev` in the above command with `tests` or `docs` respectively.


## namespace portion documentation

more info on the features and usage of this portion are available at
[ReadTheDocs](https://ae.readthedocs.io/en/latest/_autosummary/ae.updater.html#module-ae.updater
"ae_updater documentation").

<!-- common files version 0.2.77 deployed version 0.2.7 (with 0.2.77)
     to https://gitlab.com/ae-group as ae_updater module as well as
     to https://ae-group.gitlab.io with CI check results as well as
     to https://pypi.org/project/ae-updater as namespace portion ae-updater.
-->
