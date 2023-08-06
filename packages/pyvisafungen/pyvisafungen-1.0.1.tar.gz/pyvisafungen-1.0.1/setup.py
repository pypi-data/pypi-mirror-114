#!/usr/bin/env python

from setuptools import setup, find_packages
requirements = [
    "pyvisa"
]
setup(name = "pyvisafungen", version = '1.0.1',
description = "my library",
long_description = "Driver for function generators",
url = "https://github.com/users/niwotongzai/projects/1",
author = 'Kunpeng Wang',
author_email = "wangkunpeng@wipm.ac.cn",
license = "MIT Licence",
keywords = "testing testautomation",
platforms = "any",
python_requires = ">=3.5.*",
install_requires = requirements,
package_dir = {"": "src"},
packages = find_packages("src")
)

