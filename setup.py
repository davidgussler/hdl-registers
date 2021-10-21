# --------------------------------------------------------------------------------------------------
# Copyright (c) Lukas Vik. All rights reserved.
#
# This file is part of the hdl_registers project.
# https://hdl-registers.com
# https://gitlab.com/tsfpga/hdl_registers
# --------------------------------------------------------------------------------------------------

from pathlib import Path
import sys

from setuptools import setup, find_packages

REPO_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(REPO_ROOT))
PATH_TO_TSFPGA = REPO_ROOT.parent.resolve() / "tsfpga"
sys.path.insert(0, str(PATH_TO_TSFPGA))

import tsfpga
from tsfpga.system_utils import path_relative_to

import hdl_registers
from hdl_registers.about import get_readme_rst, get_slogan


REQUIREMENTS_TXT = hdl_registers.HDL_REGISTERS_PATH / "requirements.txt"
REQUIREMENTS_DEVELOP_TXT = hdl_registers.HDL_REGISTERS_PATH / "requirements_develop.txt"


def main():
    """
    Note that this script must be called from a clean repo (since all files in "tsfpga" and
    "modules" will be included; so if there are stray dirty files the will be included as well).
    Please use the "tools/build_pypi_release.py" script.

    Be extremely careful when making changes to this setup script. It is hard to see what is
    actually included and what is missing. Also the package data, and where it gets placed in the
    release tree, is very messy.

    When making changes it is recommended to try the release locally before commiting to master.
    To test in a docker image do, e.g:

    python tools/build_pypi_release.py --clean-and-build
    docker run --rm --interactive --tty --volume $(pwd)/dist:/dist:ro --workdir /dist \
        python:3.8-slim-buster /bin/bash
    python -m pip install hdl_registers-1.0.2.tar.gz

    The install should pass and you should be able to run python and "import hdl_registers".
    You should see all the files in "/usr/local/lib/python3.8/site-packages/hdl_registers".
    Check that e.g. pylintrc, vivado_settings.tcl, module_fifo.py, etc. are there.
    Test to run "python -m pip uninstall hdl_registers" and see that it passes. Check the output to
    see that there are not package files installed in weird locations (such as /usr/local/lib/).
    """
    setup(
        name="hdl_registers",
        version=hdl_registers.__version__,
        description=get_slogan(),
        long_description=get_readme_rst(include_website_link=True, verify=False),
        long_description_content_type="text/x-rst",
        license="BSD 3-Clause License",
        author="Lukas Vik",
        author_email="2767848-LukasVik@users.noreply.gitlab.com",
        url="https://hdl_registers.com",
        python_requires=">=3.6",
        install_requires=read_requirements_file(REQUIREMENTS_TXT),
        extras_require=dict(dev=read_requirements_file(REQUIREMENTS_DEVELOP_TXT)),
        packages=find_packages(),
        package_data={"hdl_registers": get_package_data()},
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "License :: OSI Approved :: BSD License",
            "Natural Language :: English",
            "Intended Audience :: Developers",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: POSIX :: Linux",
            "Topic :: Software Development :: Testing",
            "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        ],
        zip_safe=False,
    )


def read_requirements_file(path):
    requirements = []
    with open(path, encoding=tsfpga.DEFAULT_FILE_ENCODING) as file_handle:
        # Requirements file contains one package name per line
        for line_data in file_handle.readlines():
            if line_data:
                requirements.append(line_data.strip())

    return requirements


def get_package_data():
    """
    Get all files that shall be include with the release, apart from the package python files
    that are already there.
    """
    files = [REQUIREMENTS_TXT, REQUIREMENTS_DEVELOP_TXT]

    # Specify path relative to the python package folder
    package_data = [str(path_relative_to(file_path, tsfpga.TSFPGA_PATH)) for file_path in files]

    return package_data


if __name__ == "__main__":
    main()
