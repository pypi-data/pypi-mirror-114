# -*- coding: utf-8 -*-

"""
chemical_formula
A class for handling chemical formulae
"""

# Bring up the classes so that they appear to be directly in
# the checmical_formula package.

from chemical_formula.elemental_data import element_data  # noqa: F401
from chemical_formula.formula import Formula  # noqa: F401

# Handle versioneer
from ._version import get_versions

__author__ = """Paul Saxe"""
__email__ = "psaxe@molssi.org"
versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions
