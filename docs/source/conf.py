"""
Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html

Much of the autodoc/autosummary functionality here was adapted, with
huge thanks, from
https://github.com/JamesALeedham/Sphinx-Autosummary-Recursion
"""

import os
import sys

import toml


_root = os.path.abspath(os.path.join("..", ".."))
sys.path.insert(0, _root)

import simplelogincmd


_file_pyproject = os.path.join(_root, "pyproject.toml")
_pyproject = toml.load(_file_pyproject)
_poetry = _pyproject["tool"]["poetry"]


# -- Project information -----------------------------------------------------
project = "SimpleLogin-CLI"
author = _poetry["authors"][0]
release = _poetry["version"]


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
]


autosummary_generate = True
autoclass_content = "both"  # Add __init__ doc (ie. params) to class summaries
html_show_sourcelink = False  # Remove links to HTML source
autodoc_inherit_docstrings = True  # If no docstring, inherit from base class
set_type_checking_flag = True  # Enable 'expensive' imports for sphinx_autodoc_typehints
add_module_names = False  # Remove namespaces from class/method signatures

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]


# -- Options for HTML output -------------------------------------------------

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
