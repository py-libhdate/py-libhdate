"""
Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import re
import sys
from pathlib import Path

from sphinx.application import Sphinx

sys.path.insert(0, os.path.abspath("../../hdate"))


# -- Project information -----------------------------------------------------
# Variables specified below are per Sphinx documentation instructions, hence
# disabling their naming 'issues' by pylint.
# pylint: disable=invalid-name, redefined-builtin


project = "hdate"
copyright = "2016, Royi Reshef; 2017-2025, Tsvi Mostovicz"
author = "Royi Reshef"
maintainer = "Tsvi Mostovicz"

# The full version, including alpha/beta/rc tags
release = "1.1.2"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx_contributors",
    "sphinx_rtd_theme",
    "myst_parser",
]

myst_enable_extensions = ["colon_fence"]

extlinks = {
    "user": ("https://github.com/%s", "@%s"),
    "pr": ("https://github.com/py-libhdate/py-libhdate/pull/%s", "#%s"),
}


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: list[str] = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


def preprocess_markdown_files(app: Sphinx) -> None:
    """Preprocess the CHANGELOG.md Markdown file."""
    root_dir = Path(app.confdir)  # Root directory of the docs
    changelog_path = root_dir / "../../CHANGELOG.md"
    processed_path = root_dir / "CHANGELOG.md"

    content = changelog_path.read_text("utf-8")

    # Replace PRs and user mentions
    content = re.sub(r"\(#(\d+)\)", r"{pr}`\1`", content)
    content = re.sub(r"@(\w+)", r"{user}`\1`", content)

    processed_path.write_text(content, "utf-8")

    print(f"Processed {changelog_path} -> {processed_path}")


def setup(app: Sphinx) -> None:
    """Setup the Sphinx app."""
    app.connect("builder-inited", preprocess_markdown_files)
